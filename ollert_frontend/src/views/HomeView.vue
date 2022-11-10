<script>
import CardLists from '../components/CardLists.vue';
async function getCardLists() {
	var raw_lists = await fetch("http://" + import.meta.env.VITE_DATABASE_URL + "/cardlist-list/");

	let x = await raw_lists.json();

	console.log(x);

	return x;
};


export default {
	methods: {
		async makeNewCardList() {
			await fetch("http://" + import.meta.env.VITE_DATABASE_URL + "/cardlist-create/", {
				method: "POST",
				headers: {
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
					"name": "Liste",
				})
			});
			console.log("Posted");
		},
	},
	data() {
		return {
			"cardLists": [],
			"currentPositionList": NaN, // The current list being hovered over
			"currentPositionRow": NaN, // The current card/row being hovered over
			"movingCardList": NaN, // The list of the card currently being moved; If NaN no card is being moved.
			"movingCardRow": NaN, // The row of the card currently being moved; If NaN no card is being moved.
		};
	},
	async mounted() {

		document.addEventListener('mouseup', this.mouseReleased, true)
		this.cardLists = await getCardLists();
	},
	components: { CardLists },
	methods: {
		moveCard(list, row) {
			// console.log(list, row);

			this.currentPositionList = list;
			this.currentPositionRow = row;

			// console.log(this.cardLists[list].cards[row].name);
		},
		mouseLeft(list, row) {
			if (this.currentPositionList == list && this.currentPositionRow == row) {
				// console.log("Left " + list + "-" + row)
				this.currentPositionList = NaN;
				this.currentPositionRow = NaN;
			} else {
				console.log("Could not leave")
			}
		},
		selectCard(list, row) {
			this.movingCardList = list;
			this.movingCardRow = row;
		},
		mouseReleased(pos) {
			if (!isNaN(this.currentPositionList)) {
				console.log("Moving card to", this.currentPositionList, this.currentPositionRow);


				this.postMoveCard(this.currentPositionList, this.currentPositionRow, this.movingCardList, this.movingCardRow)

				// try {
				// 	// console.log(this.cardLists, "[", this.currentPositionList, "].cards.insert(", this.currentPositionRow, ", ", this.cardLists[this.movingCardList].cards[his.movingCardRow]);
				// 	let cardlist = this.cardLists.at(this.currentPositionList);
				// 	console.log("cardlist:", cardlist);
				// 	if (cardlist != undefined) {
				// 		let cards = cardlist.cards;
				// 		let movingcard = this.cardLists.at(this.movingCardList).cards.at(this.movingCardRow);
				// 		cards.splice(0, this.currentPositionRow, movingcard);
				// 		console.log("cards:", cards)
				// 	}
				// } catch (e) {
				// 	console.log(e);

				// }
			}
		},
		async postMoveCard(list, row, from_list, from_row) {
			let raw_lists = await fetch("http://" + import.meta.env.VITE_DATABASE_URL + "/card-move/", {
				method: "POST",
				headers: {
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
					"card_id": this.cardLists[from_list].cards[from_row].id, // Cards id
					"list_id": this.cardLists[list].id, // Lists id
					"row": row, // Position in list.
				})
			});

			let x = await raw_lists.json();
			this.cardLists = x
			console.log(x);
		}
	}
}
</script>

<template>

	<body @mousemove="">
		<br>
		<button type="button" @click="makeNewCardList()">
			bruh
		</button>
		<div class="card-list-holder">
			<CardLists v-for="x, i in cardLists" :name="x.name" :items="x.cards" :indent="i" @mouse-entered="moveCard"
				@mouse-left="mouseLeft" @select-card="selectCard">

			</CardLists>
		</div>
	</body>
</template>

<style>
body {
	background-color: #222;
}

div.card-list-holder {
	display: flex;
}
</style>