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
		mouseEntered(indent, isCard) {
			if (isCard) {
				this.currentPositionRow = indent;
			} else if (!isCard) {
				this.currentPositionList = indent;
			}

			// console.log(this.cardLists[list].cards[row].name);
		},
		mouseLeft(indent, leavingCard) {
			if (this.currentPositionList == indent && !leavingCard) {
				this.currentPositionList = NaN;
			} if (this.currentPositionRow == indent && leavingCard) {
				this.currentPositionRow = NaN;
			}
		},
		selectCard(list, row) {
			this.movingCardRow = row;
			this.movingCardList = list;
			console.log("Selecting", row, list);
		},
		mouseReleased(pos) {
			if (!isNaN(this.currentPositionList)) {
				console.log("Moving card to", this.currentPositionList, this.currentPositionRow);
				this.postMoveCard(this.currentPositionList, this.currentPositionRow, this.movingCardList, this.movingCardRow)
			}
		},
		async postMoveCard(list, row, from_list, from_row) {
			let body = {
				"card_id": this.cardLists[from_list].cards[from_row].id, // Cards id
				"list_id": this.cardLists[list].id, // Lists id
			}

			if (!isNaN(row)) {
				body["row"] = row;
			}

			console.log(body);


			let raw_lists = await fetch("http://" + import.meta.env.VITE_DATABASE_URL + "/card-move/", {
				method: "POST",
				headers: {
					"Accept": "application/json",
					"Content-Type": "application/json"
				},
				body: JSON.stringify(body)
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
			<CardLists v-for="x, i in cardLists" :name="x.name" :items="x.cards" :indent="i"
				@mouse-entered="mouseEntered" @mouse-left="mouseLeft" @select-card="selectCard">

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