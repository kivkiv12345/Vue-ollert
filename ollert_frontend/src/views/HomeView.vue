<script>
var cardLists = [];
export default {

	async getCardLists() {
		var raw_lists = await fetch("http://localhost:8000/api/cardlist-list/?format=json");

		console.log(raw_lists);
	},
	data() {
		getCardLists();
		return {}
	}
}
</script>

<template>

</template>
