<template>
    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>
</template>

<script setup>
import 'primeicons/primeicons.css'
</script>

<style>
body{
    margin: 0;
    padding: 0;
}
::-webkit-scrollbar {
    display: none;
}

.p-listbox-list-container{
    max-height: 100%!important;
}
.p-dataview-content, .p-dataview-empty-message{
    height: inherit;
    background: transparent!important;
}
</style>

<style>
html{
    overflow-x: hidden;
    width: 100vw;
    height: 100vh;
    padding: 0px;
    margin: 0px;
}
:root {
    --p-datatable-sort-icon-color: white!important;
    --p-datatable-sort-icon-hover-color:white!important;
    --p-datatable-row-selected-background: gray!important;
}
.p-datatable-column-filter-button{
    color: white!important;
}
.p-datatable-column-filter-button:hover{
    color: gray!important;
}
tbody .p-datatable-frozen-column{
    background: inherit!important;
}

#main-upload .p-fileupload-header{  
    display: none!important;  
} 

/* */
.image-description{
    width: 750px; 
    height: 470px;
    margin: 2rem; 
    margin-left: 10%; 
    border-radius: 20px;
}

/**/
.html-visualizer p{
    margin: 1.5px!important;
}
.html-visualizer table{
    border-collapse: inherit!important;
    width: 100%!important;
}
.html-visualizer td, th{
    border: 1px solid gray!important;
    padding: 5px 3px!important;
}

.html-visualizer h1, .html-visualizer h2, .html-visualizer h3, .html-visualizer h4, .html-visualizer h5, .html-visualizer h6 {
    font-size: revert!important;
    font-weight: revert!important;
}
.html-visualizer img, .html-visualizer svg, .html-visualizer video, .html-visualizer canvas, .html-visualizer audio, .html-visualizer iframe, .html-visualizer embed, .html-visualizer object {
    display: revert!important;
    vertical-align: revert!important;
}
.html-visualizer * {
    width: auto !important;
    height: auto !important;
    max-width: 100% !important;
    max-height: 100% !important;
    box-sizing: border-box;
}
</style>