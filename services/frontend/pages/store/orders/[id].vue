<template>
    <ViewOrderDetailComponent :order-number="route.params.id.toString()" :show-bread-crumb="true" :force-update="true"/>
</template>

<script lang="ts" setup>
    // Meta configuration
    definePageMeta({
        layout:'public'
    });
    const route=useRoute();

</script>
