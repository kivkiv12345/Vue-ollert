

<template>
    <Transition name="modal">
        <div class="Mask" v-if="show" @click="$emit('close')">
            <div class="wrapper">
                <div class="modal" @click.stop>
                    <h1 v-if="making != undefined">
                        New {{ making }}
                    </h1>
                    <form @submit.prevent="submit">
                        <div v-for="value, key in fields">
                            <div v-if="key != 'id'" class="form-field">
                                <label v-bind:for="key + '_input_field'">{{ capitalizeFirstLetter(key) }}</label>
                                <input v-bind:type="getTypeOfInput(value)" v-bind:id="key + 'input_field'"
                                    v-bind:name="key">
                            </div>
                        </div>
                        <div style="height: 20px"></div>
                        <input type="submit" id="SubmitButton" value="Send" />


                    </form>

                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { def } from '@vue/shared';

defineProps({
    making: {
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
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


function getTypeOfInput(value) {
    let type = value['internalType'].toLowerCase();
    if (type.includes("integer")) {
        return "number";
    }
    return "text"
}

function get_url() {
    return (import.meta.env.VITE_DATABASE_URL == undefined || import.meta.env.VITE_DATABASE_URL == "" ? location.hostname : import.meta.env.VITE_DATABASE_URL) + ":8000/api";
}

export default {
    methods: {
        async get_fields() {
            if (this.making == undefined) {
                return;
            }
            let raw_lists = await fetch("http://" + get_url() + "/" + this.making + "/", {
                method: "GET",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
            });
            let x = await raw_lists.json();
            this.fields = x;
        },
        async submit(formData) {

            console.log(this.fields)
            console.log(formData.target.elements)

            let body = new Map()

            console.log(this.fields)

            for (const key in this.fields) {
                if (formData.target.elements.hasOwnProperty(key)) {
                    let value = eval("formData.target.elements." + key).value;
                    let _key = eval("this.fields." + key)
                    console.log(_key.internalType.toLowerCase())
                    if (_key.internalType.toLowerCase().includes("integer"))
                        body.set(key, parseInt(value));
                    else
                        body.set(key, value)
                }
            }
            body.set("cards", [])

            let jsonBody = JSON.stringify(Object.fromEntries(body));

            console.log("x", jsonBody);

            let response = await fetch("http://" + get_url() + "/" + this.making + "-create/", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: jsonBody
            });
        }
    },
    data() {
        return {
            "fields": null,
        }
    },
    mounted() {
        console.log(this.show);
        console.log("Fishsticks")

        this.get_fields();
    },
    watch: {
        making(curr, prev) {
            console.log("Meatsticks")
            if (curr != "" && curr != undefined) {
                this.get_fields()
            }
        }
    }
}
</script>
<style>
div.modal {
    background-color: bisque;
    min-height: 200pt;
    margin: 0 100pt;

    border-radius: 8pt;

    display: flexbox;
    padding: 20px;
}

div.wrapper {
    display: table-cell;
    vertical-align: middle;
}

div.form-field {
    display: grid;
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