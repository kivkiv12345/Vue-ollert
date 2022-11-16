<script setup>
defineProps({
    name: {
        type: String,
        required: false,
    },
    row: {
        type: Number,
        required: true,
    },
    indent: {
        type: Number,
        required: true,
    },
    order: {
        type: Number,
        required: false,
    },
    description: {
        type: String,
        required: false,
    },
    selected: {
        type: Boolean,
        required: true
    },
    moving: {
        type: Boolean,
        required: true,
    }
})
</script>

<script>

export default {
    emits: [
        "mouseEntered",
        "mouseLeft",
        "selectCard",
    ],
    data() {
        return {
            "body_id": "card-" + this.row + "-" + this.indent,
        }
    },
    mounted() {
        let body = document.getElementById(this.body_id);
        body.addEventListener('mouseenter', this.mouseEnter);
        body.addEventListener('mouseleave', this.mouseLeft);
        body.addEventListener('mousedown', this.selectCard);
    },
    methods: {
        mouseEnter(pos) {
            // console.log(this.row + "-" + this.indent);
            this.$emit("mouseEntered", this.indent);
        },
        mouseLeft(pos) {
            this.$emit("mouseLeft", this.indent);
        },
        selectCard(pos) {
            this.$emit('selectCard', this.indent);
        },
    }
}
</script>

<template>
    <div v-bind:id="body_id" class="body">
        <div v-if="selected && !moving" class="body body-color" style="margin-bottom: 5pt !important;">

        </div>
        <div v-bind:class="moving ? 'ghost body body-color' : 'body body-color'">
            <div>
                <h4 class="card-header">
                    {{ order }}
                    {{ name }}
                </h4>
                <p class="description" v-if="description != undefined">

                    {{ description }}
                </p>
            </div>
        </div>
    </div>
</template>

<style>
div.ghost {
    background-color: grey !important;
}

div.body-color {
    background-color: burlywood;
    margin: 0pt !important;
}

div.body {
    border-radius: 5pt;
    min-height: 20pt;
    padding-top: 5px;
    padding-bottom: 5px;
}

.card-header {
    background-color: antiquewhite;
    border-radius: 5pt;
    padding: 5px;
    padding-left: 10pt;
    margin: 5px;
    margin-top: 1pt;
    margin-bottom: 0;
}

p.description {
    padding: 4pt;
    background-color: antiquewhite;
    border-radius: 5pt;
    margin: 5px;
    margin-bottom: 0;
    text-overflow: ellipsis;
}
</style>