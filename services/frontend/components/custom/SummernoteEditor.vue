<template>
    <div class="editor">
        <textarea ref="summernote"></textarea>
    </div>
</template>
  
<script>
export default {
    props: {
        modelValue: {
            type: String,
            default: ''
        },
        placeholder: {
            type: String,
            default: 'Escribe algo aquí...'
        },
        height: {
            type: Number,
            default: 400
        },
        options: {
            type: Object,
            default: () => ({})
        }
    },
    watch: {
        modelValue(newValue) {
            if (typeof window !== 'undefined' && typeof window.$ !== 'undefined') {
                if (newValue !== $(this.$refs.summernote).summernote('code')) {
                    $(this.$refs.summernote).summernote('code', newValue);
                }
            }
        }
    },
    mounted() {
        this.initializeSummernote();
    },
    beforeUnmount() {
        if (typeof window !== 'undefined' && typeof window.$ !== 'undefined') {
            $(this.$refs.summernote).summernote('destroy');
        }
    },
    methods: {
        initializeSummernote() {
            if (typeof window !== 'undefined' && typeof window.$ !== 'undefined') {
                /*$.ajax({
                    url: 'https://api.github.com/emojis',
                    async: false 
                }).then(function(data) {
                    window.emojis = Object.keys(data);
                    window.emojiUrls = data; 
                });*/

                $(this.$refs.summernote).summernote({
                    height: this.height,
                    placeholder: this.placeholder,
                    
                    ...this.options,
                    callbacks: {
                        onChange: (contents) => {
                            this.$emit('update:modelValue', contents);
                        }
                    },

                    toolbar: [
                        ['style',['style']],
                        ['font',['bold','italic','underline', 'clear']],
                        ['fontname',['fontname']],
                        ['fontsize', ['fontsize']],
                        ['color',['color']],
                        ['para',['', 'ul','ol','paragraph']],
                        ['table',['table']],
                        ['insert', ['link', 'picture']],

                        ['view',['codeview']],
                        ['help',['help']]
                    ],
                    lang: 'es-ES',
                    fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Merriweather'],
                    addDefaultFonts: false,
                    fontNamesIgnoreCheck: ['Merriweather'],

                    codemirror: { 
                        theme: 'monokai',      
                        lineNumbers: true,     
                        lineWrapping: true,   
                        indentUnit: 2        
                    },
                    /*hint: {
                        match: /:([\-+\w]+)$/,
                        search: function (keyword, callback) {
                            callback($.grep(emojis, function (item) {
                                return item.indexOf(keyword)  === 0;
                            }));
                        },
                        template: function (item) {
                            var content = emojiUrls[item];
                            return '<img src="' + content + '" width="20" /> :' + item + ':';
                        },
                        content: function (item) {
                            var url = emojiUrls[item];
                            if (url) {
                                return $('<img />').attr('src', url).css('width', 20)[0];
                            }
                            return '';
                        }
                    },*/
                });
                $(this.$refs.summernote).summernote('code', this.modelValue);

            } else {
                console.error('jQuery or Summernote not found');
            }
        }
    }
};
</script>

<style>
    .editor td, th{
        border-color: gray!important;
    }
    .editor h1, .editor h2, .editor h3, .editor h4, .editor h5, .editor h6 {
        font-size: revert!important;
        font-weight: revert!important;
    }
    .editor img, .editor svg, .editor video, .editor canvas, .editor audio, .editor iframe, .editor embed, .editor object {
        display: revert!important;
        vertical-align: revert!important;
    }
</style>

<style scoped>
    @import url('https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/codemirror.min.css');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/theme/monokai.min.css');
</style>
  