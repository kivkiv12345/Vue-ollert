

<template>
    <Transition name="modal">
        <div class="Mask" v-if="show" @click="$emit('close')">
            <div class="wrapper">
                <div class="modal">
                    <form>
                        <div v-for="value, key in fields">
                            <input type="getTypeOfInput(value)" \>

                            {{ key }}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { def } from '@vue/shared';

defineProps({
    field_type: {
        type: String,
        required: true,
    },
    show: {
        type: Boolean,
        required: true,
    },
})
</script>
<script>
function getTypeOfInput(value) {
    let type = value['internalType'].toLower();
    if (type.contains("integer")) {
        return "number";
    }
}

export default {
    methods: {
        async get_fields() {
            let raw_lists = await fetch("http://" + import.meta.env.VITE_DATABASE_URL + "/" + this.field_type + "/", {
                method: "GET",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
            });
            let x = await raw_lists.json();

            this.fields = x;
        }
    },
    data() {
        return {
            "fields": null,
        }
    },
    mounted() {
        console.log(this.show);

        this.get_fields();
    }
}
</script>
<style>
div.modal {
    background-color: bisque;
    min-height: 200pt;
    margin: 0 100pt;

    border-radius: 8pt;

    display: flex;
}

div.wrapper {
    display: table-cell;
    vertical-align: middle;
}

div.Mask {
    position: fixed;
    z-index: 100000;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: table;
    align-content: center;
}
</style>