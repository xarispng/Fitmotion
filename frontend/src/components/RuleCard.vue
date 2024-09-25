<template>
    <div class="rule-card">
        <h3>{{ title }}</h3>
        <p v-if="text">
            <i class="mdi mdi-exclamation"></i> {{ text }}
        </p>
    </div>
</template>

<script>
    import '@mdi/font/css/materialdesignicons.min.css';

    export default {
        name: 'RuleCard',
        props: {
            title: {
                type: String,
                required: false
            },
            text: {
                type: String,
                required: true
            },
        }
    }
</script>

<style scoped>
    @import '../styles/RuleCard.css'; 
</style>