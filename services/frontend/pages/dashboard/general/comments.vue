<template>
    <div class="my-6 flex flex-col gap-4" v-if="filteredCommentData.length > 0">
        <div class="flex flex-row gap-4 m-2 p-4 shadow-lg rounded-lg" v-for="(comment, index) in filteredCommentData" :key="comment.id">
            <div class="basis-[4rem]">
                <Avatar image="/avatar.png" class="mr-2" size="large" shape="circle" />
            </div>

            <div class="flex-1 flex flex-col gap-4">
                <div class="flex flex-row flex-wrap gap-4">
                    <div class="basis-full md:basis-[80%] flex flex-row flex-wrap gap-4">
                        <span :class="isMobile?'basis-[52%]':''" class="truncate text-gray-500 uppercase text-lg">{{ comment.responsible__username }}</span>
                        <Rating readonly v-model="comment.starts" />
                        <i v-if="isMobile" @click="openMenu($event, comment, index)" class="flex md:hidden w-0 text-right pi pi-ellipsis-v cursor-pointer mt-2"></i>

                        <span class="px-3 h-6 rounded-md pt-[2px] bg-orange-500 text-white text-sm">{{ comment.product__title ? comment.product__title : comment.service__title }}</span>
                        <span v-if="comment.deleted" class="px-3 h-6 rounded-md pt-[2px] bg-red-500 text-white text-sm">Eliminado</span>
                    </div>

                    <span v-if="!isMobile" v-tooltip.top="dayjs(comment.creation_date).format('YYYY-MM-DD HH:mm:ss')" class="flex-1 mt-2 text-center text-gray-500 text-sm">{{dayjs(comment.creation_date).fromNow() }}</span>
                    <i v-if="!isMobile" @click="openMenu($event, comment, index)" class="w-5 text-center pi pi-ellipsis-v cursor-pointer mt-2"></i>
                </div>

                <div class="html-visualizer" v-html="comment.description"></div>
            </div>
        </div>
    </div>

    <div class="py-40" v-else>
        <svg-icon class="block text-gray-400/[0.8] w-full text-center" size="70" type="mdi" :path="mdiForumOutline"></svg-icon>
        <span class="mt-4 mx-10 block text-2xl text-gray-400/[0.8] text-center font-medium">Aún no hay comentarios para mostrar.</span>
    </div>

    <Menu ref="commentMenu" id="overlay_menu" :model="itemsMenu" :popup="true" />
    <Toast />
    <ConfirmDialog></ConfirmDialog>
</template>

<script lang="ts" setup>
    import {cloneDeep} from 'lodash-es';

    import dayjs from 'dayjs';
    import relativeTime from 'dayjs/plugin/relativeTime';
    import locale_es from 'dayjs/locale/es';
    import {fetchWrapper} from "~/helpers/fetch-wrapper";
    import { mdiForumOutline } from '@mdi/js';
    import type { CommentItem } from '~/types/dashboard/comments';
    import { useMediaQuery } from '@vueuse/core';

    /********************* 
    | Setup Configuration
    **********************/
    const confirm = useConfirm();
    const toast = useToast();
    
    dayjs.extend(relativeTime);
    dayjs.locale('es');
    
    useListen('application:search' , (message:any) => {
        const search = (message.message as string).toLowerCase();
        filteredCommentData.value=commentData.value.filter(entry=>{
            return (
                entry.description.toLowerCase().includes(search) ||
                entry.starts.toString().includes(search) ||
                entry.product__title.toLowerCase().includes(search) ||
                entry.responsible__username.toString().includes(search) ||
                entry.deleted.toString().includes(search)
            );
        });
    });
    const isMobile = useMediaQuery('(max-width: 600px)');

    /********************* 
    | Data
    **********************/
    const itemsMenu = ref([{
        label: 'Opciones',
        items: [
            {
                label: 'Eliminar',
                icon: 'pi pi-trash',
                command: () => {
                    doDelete(selectedComment.value.id, selectedIndex.value);
                }
            }
        ]
    }]);

    const commentData=ref<CommentItem[]>([]);
    const filteredCommentData=ref<CommentItem[]>([]);

    const commentMenu = ref();
    const selectedComment = ref<CommentItem>({
        id: -1,
        description: '',
        starts: -1,
        creation_date: '',
        product__title: '',
        service__title: '',
        responsible__id: -1,
        responsible__username: '',

        deleted: false
    });
    const selectedIndex = ref<number>(-1);

    /********************* 
    | Actions
    **********************/
    const openMenu = ($event:MouseEvent, comment:CommentItem, index:number) => {
        selectedComment.value = comment;
        selectedIndex.value = index;
        commentMenu.value.toggle($event);
    };

    const doDelete = async (id:number, index:number) =>{
        confirm.require({
            message: "¿Seguro(a) que quieres eliminar este registro?",
            header: "Confirmar eliminación",
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
            accept: async function(){
                const params = new URLSearchParams();
                params.append('comment_ids', JSON.stringify([id]));

                await fetchWrapper.delete('/comments/batch?'+params).then(async (response)=>{
                    toast.add({ severity: 'success', summary: 'Confirmación', detail: JSON.stringify(response), life: 5000 });
                    const keys=[id.toString()];
                    filteredCommentData.value=filteredCommentData.value.filter(item => keys.indexOf(item.id.toString()) === -1);
                    commentData.value=filteredCommentData.value.filter(item => keys.indexOf(item.id.toString()) === -1);
                }).catch((e)=>{
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Error al eliminar: '+JSON.stringify(e), life: 7000 });
                });
            }
        });
    };
    /********************* 
    | MOUNT
    **********************/
    onMounted(async ()=>{
        commentData.value=await fetchWrapper.get('/comments/comments');
        filteredCommentData.value=cloneDeep(commentData.value);
    });
</script>