<template>
    <div class="flex flex-col p-2 md:p-4">
        <span class="text-2xl pt-4 font-medium">{{ countComments }} Reseña(s)</span>
        <Message class="my-4" severity="success">
            Todas las reseñas son de compras verificadas
            <template #icon>
                <svg-icon class="icon" size="24" type="mdi" :path="mdiShieldCheckOutline"></svg-icon>
            </template>
        </Message>

        <div class="my-2 flex flex-col gap-4">
            <div class="my-6 flex flex-col gap-4" v-if="comments.length > 0">
                <div class="flex flex-row gap-4 m-0 md:m-2 p-2 md:p-4 shadow-lg rounded-lg" v-for="(comment, index) in comments" :key="comment.id">
                    <div class="basis-[4rem]">
                        <Avatar image="/avatar.png" class="mr-2" size="large" shape="circle" />
                    </div>

                    <div class="flex-1 flex flex-col gap-4">
                        <div class="flex flex-row gap-4">
                            <div class="basis-[80%] flex flex-col md:flex-row gap-1 md:gap-4">
                                <span class="text-gray-500 uppercase text-lg">{{ comment.responsible__username }}</span>
                                <Rating readonly v-model="comment.starts" />
                            </div>

                            <span class="hidden md:!block flex-1 mt-2 text-center text-gray-500 text-sm" v-tooltip.top="dayjs(comment.creation_date).format('YYYY-MM-DD HH:mm:ss')">{{dayjs(comment.creation_date).fromNow() }}</span>
                            <i v-if="user?.username && comment.responsible__id === user?.id" @click="openMenu($event, comment, index)" class="w-5 text-center pi pi-ellipsis-v cursor-pointer mt-2"></i>
                        </div>

                        <div class="comment html-visualizer" v-html="comment.description"></div>
                    </div>
                </div>
            </div>

            <div class="py-20" v-else>
                <svg-icon class="block text-gray-400/[0.8] w-full text-center" size="70" type="mdi" :path="mdiForumOutline"></svg-icon>
                <span class="mt-4 mx-0 md:mx-10 block text-2xl text-gray-400/[0.8] text-center font-medium">Aún no hay comentarios para este {{ props.isService ? 'servicio':'producto' }}. Sé uno de los primeros en comentar.</span>
            </div>

            <div class="text-center" v-if="countComments > 4">
                <Button @click="showAllComments" icon="pi pi-eye" label="Ver todos los comentarios"/>
            </div>
        </div>

        <div class="mt-8 flex flex-col gap-4" v-if="user?.username">
            <span class="font-bold text-lg">Califica este {{ props.isService ? 'servicio':'producto' }}:</span>
            <SummernoteEditor placeholder="Escribe un comentario..." :height="250" v-model="commentForm.description"/>

            <div class="flex flex-row gap-4">
                <div class="basis-[50%] md:basis-[80%] flex flex-row gap-1 md:gap-4">
                    <Rating class="h-icon" v-model="commentForm.starts" />
                    <span class="hidden md:block text-lg mt-2">{{commentForm.starts === null ? qualifications[0] : qualifications[commentForm.starts]}}</span> 
                </div>

                <Button @click="saveComment" :loading="commentLoading" :disabled="commentLoading || (commentForm.starts === null || commentForm.starts === -1) || commentForm.description === '' " class="flex-1" icon="pi pi-pencil" label="Comentar"/>
            </div>
        </div>

        <div class="flex flex-col gap-4 my-14" v-else-if="!user?.username">
            <span class="w-full text-center text-2xl font-medium text-gray-500/[0.8] ">No estás logeado(a)</span>
            <span class="w-auto md:w-96 mx-auto text-center text-gray-500/[0.8] text-lg">
                Inicia Sesión o registrate para poder añadir un comentario.
            </span>
            
            <Button @click="openLoginRegisterClientModal" class="w-auto md:w-96 mx-auto" icon="pi pi-sign-in" label="Iniciar Sesión" />
        </div>
    </div>

    <Dialog class="w-[45rem]" :draggable="false" v-model:visible="showMoreComments" modal :closable="false" :dismissable-mask="true">
        <div class="my-6 flex flex-col gap-4">
            <div class="flex flex-row gap-4 m-2 p-4 shadow-lg rounded-lg" v-for="(comment, index) in allComments" :key="comment.id">
                <div class="basis-[4rem]">
                    <Avatar image="/avatar.png" class="mr-2" size="large" shape="circle" />
                </div>

                <div class="flex-1 flex flex-col gap-4">
                    <div class="flex flex-row gap-4">
                        <div class="basis-[65%] flex flex-row gap-4">
                            <span class="text-gray-500 uppercase text-lg">{{ comment.responsible__username }}</span>
                            <Rating readonly v-model="comment.starts" /> 
                            <span class="text-base hidden md:!block ">{{comment.starts === null ? qualifications[0] : qualifications[comment.starts]}}</span>
                        </div>

                        <span v-tooltip.top="dayjs(comment.creation_date).format('YYYY-MM-DD HH:mm:ss')" class="hidden md:!block flex-1 mt-2 text-center text-gray-500 text-sm">{{dayjs(comment.creation_date).fromNow() }}</span>
                    </div>
                    <div class="html-visualizer" v-html="comment.description"></div>
                </div>
            </div>
        </div>
    </Dialog>

    <Menu ref="commentMenu" id="overlay_menu" :model="itemsMenu" :popup="true" />
    <Toast />
    <ConfirmDialog></ConfirmDialog>
</template>

<script lang="ts" setup>
    import {ref, type UnwrapRef, defineProps} from 'vue';
    import { mdiForumOutline, mdiShieldCheckOutline} from '@mdi/js';
    import { useMediaQuery } from '@vueuse/core';

    import { useConfirm } from "primevue/useconfirm";
    import { useToast } from "primevue/usetoast";
    import dayjs from 'dayjs';
    import relativeTime from 'dayjs/plugin/relativeTime';
    import locale_es from 'dayjs/locale/es'
    import {cloneDeep} from 'lodash-es';
    import {qualifications} from '~/helpers/constants'
    import {fetchWrapper} from "~/helpers/fetch-wrapper";
    import type {CommentItem, CommentForm} from '~/types/dashboard/comments';
    import {useAuthStore} from '~/stores/auth.store';

    // Meta configuration
    definePageMeta({
        layout:'public'
    });

    function resetFields(){
        commentForm.description='';
        commentForm.product='';
        commentForm.starts=-1;
    };

    const authStore=useAuthStore();
    dayjs.extend(relativeTime);
    dayjs.locale('es');

    const props = defineProps<{ readonly itemId: string, isService: boolean}>();
    const {user} = storeToRefs(authStore);
    const isMobile = useMediaQuery('(max-width: 600px)');
    const confirm = useConfirm();
    const toast = useToast();

    /********************* 
    | DATA
    **********************/
    const itemsMenu = ref([{
        label: 'Opciones',
        items: [
            {
                label: 'Editar',
                icon: 'pi pi-pencil',
                command: () => {
                    doAction('edit', selectedComment.value.id.toString(), selectedIndex.value);
                }
            },
            {
                label: 'Eliminar',
                icon: 'pi pi-trash',
                command: () => {
                    doAction('delete', selectedComment.value.id.toString(), selectedIndex.value);
                }
            }
        ]
    }]);

    // Main
    const commentForm:UnwrapRef<CommentForm> = reactive({
        description: '',
        product: '',
        service: '',
        starts: -1
    });
    const commentMenu = ref();
    const selectedComment = ref<CommentItem>({
        id: -1,
        description: '',
        starts: -1,
        creation_date: '',
        service__title: '',
        product__title: '',
        responsible__id: -1,
        responsible__username: '',

        deleted: false
    });
    const selectedIndex = ref<number>(-1);
    const showMoreComments = ref<boolean>(false);

    // Header
    const commentLoading = ref<boolean>(false);
    const currentCommentIndex = ref<number>(-1);
    const currentCommentId = ref<string>('-1');
    const countComments=ref<number>(0);
    const comments=ref<CommentItem[]>([]);
    const allComments=ref<CommentItem[]>([]);
    
    /********************* 
    | METHODS
    **********************/
    //
    const openLoginRegisterClientModal= (event:any)=>{
        sendEvent('modal:login-register-client', {severity: 'normal', message: ''});
    };

    const openMenu = ($event:MouseEvent, comment:CommentItem, index:number) => {
        selectedComment.value = comment;
        selectedIndex.value = index;
        commentMenu.value.toggle($event);
    };
    //Header
    const doAction = async(action:string, id:string, index:number)=>{
        if (["new", "edit"].indexOf(action) > -1){
            if (action === "new"){
                resetFields();
            }else{
                const data:CommentItem=comments.value[index];
                commentForm.starts=data.starts;
                commentForm.description=data.description;
            }
            currentCommentId.value=id;
            currentCommentIndex.value=index;
        }else{
            confirm.require({
                message: "¿Seguro(a) que quieres eliminar este comentario?",
                header: "Esta accion no se puede deshacer. ¿Continuar?",
                icon: 'pi pi-info-circle',
                rejectLabel: 'Cancelar',
                rejectProps: {
                    label: 'Cancelar',
                    severity: 'secondary',
                    outlined: true
                },
                acceptProps: {
                    label: 'Confirmar',
                    severity: 'danger'
                },
                accept: async()=>{
                    const params = new URLSearchParams();
                    params.append('comment_id', id);

                    await fetchWrapper.put('/comments/delete?'+params).then(async (response)=>{
                        toast.add({ severity: 'success', summary: 'Éxito', detail: response["msg"], life: 5000 });
                       
                        const params=new URLSearchParams();
                        params.append('product_id', props.itemId.toString());
                        params.append('initial', '1');
                        const data=await fetchWrapper.get('/comments/public?'+params);
                        comments.value=data["comments"];
                        countComments.value=countComments.value-1;
                    }).catch((e)=>{
                        toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(e), life: 7000 });
                    });
                }
            });
        }
    }

    // CRUD Actions
    const saveComment = async () => {
        commentLoading.value = true;
        commentForm.product=props.isService? '':props.itemId.toString();
        commentForm.service=props.isService? props.itemId.toString():'';
        commentLoading.value=true;

        const action=currentCommentIndex.value === -1 ? fetchWrapper.post:fetchWrapper.put;
        const query= currentCommentIndex.value === -1 ? '':'?comment_id='+currentCommentId.value;

        await action('/comments/save'+query, commentForm, { credentials: 'include' }).then(async (response) => {
            if (currentCommentIndex.value === -1){
                comments.value.unshift(response["data"]);
                comments.value=comments.value.slice(0, 5);
                countComments.value=countComments.value+1;
            }else{
                commentLoading.value=false;   
                comments.value[currentCommentIndex.value]=cloneDeep(response["data"]);
            }

            toast.add({ severity: 'success', summary: 'Éxito', detail: response["msg"], life: 5000 });
            commentLoading.value=false;
            resetFields();
            currentCommentId.value='-1';
            currentCommentIndex.value=-1;
        }).catch((e) => {
            toast.add({ severity: 'error', summary: 'Error', detail: JSON.stringify(e), life: 7000 });
            commentLoading.value = false;
            commentLoading.value=false;
        });
    }

    const showAllComments = async()=>{
        const params=new URLSearchParams();
        params.append('product_id', props.itemId.toString());
        params.append('initial', '0');
        const commentData=await fetchWrapper.get('/comments/public?'+params);
        allComments.value=commentData["comments"];
        countComments.value=parseInt(commentData["count"]);
        
        showMoreComments.value=true;
    }
    /********************* 
    | MOUNT
    **********************/
    onMounted(async()=>{
        const params=new URLSearchParams();
        params.append('item_id', props.itemId.toString());
        params.append('initial', '1');
        params.append('is_service', props.isService?'1':'0');

        const commentData=await fetchWrapper.get('/comments/public?'+params);
        comments.value=commentData["comments"];
        countComments.value=parseInt(commentData["count"]);
    });
</script>

<style>
.h-icon svg{
    width: 1.5rem;
    height: 1.5rem;
}

@media (max-width: 600px) {
    .comment{
        width: 12rem;
    }
}
</style>