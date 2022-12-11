<script>
	import CardLists from '../components/CardLists.vue';
	import NewOverlay from '../components/NewOverlay.vue';

	async function getCardLists() {
		var raw_lists = await fetch("http://" + get_url() + "/cardlist-list/");


		let x = await raw_lists.json();

		console.log(x);

		return x;
	};


	function get_url() {
		return (import.meta.env.VITE_DATABASE_URL == undefined || import.meta.env.VITE_DATABASE_URL == "" ? location.hostname : import.meta.env.VITE_DATABASE_URL) + ":8000/api";
	}

	export default {
		async mounted() {

			document.addEventListener('mouseup', this.mouseReleased, true)
			this.cardLists = await getCardLists();
		},
		data() {
			return {
				"cardLists": [],
				"currentPositionList": NaN, // The current list being hovered over
				"currentPositionRow": NaN, // The current card/row being hovered over
				"movingCardList": NaN, // The list of the card currently being moved; If NaN no card is being moved.
				"movingCardRow": NaN, // The row of the card currently being moved; If NaN no card is being moved.

				"showModal": false,
				"making": undefined, // This is passed to the "new item" modal popup to tell it what the user is trying to make a new of
			};
		},
		components: { CardLists, NewOverlay },
		methods: {
			makeNewCardList() {
				this.making = "cardlist"
				this.showModal = true;
			},
			async exitModal() {
				if (this.making == "cardlist") {
					this.cardLists = await getCardLists()
				}

				this.making = undefined
				this.showModal = false
			},
			mouseEntered(indent, isCard) {
				if (isCard) {
					console.log("Settings position row", indent)
					this.currentPositionRow = indent;
				} else if (!isCard) {
					console.log("Settings position list", indent)
					this.currentPositionList = indent;
				}
			},
			mouseEntered(indent, isCard) {
				if (isCard) {
					console.log("Settings position row", indent)
					this.currentPositionRow = indent;
				} else if (!isCard) {
					console.log("Settings position list", indent)
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
				try {
					let body = {
						"card_id": this.cardLists[from_list].cards[from_row].id, // Cards id
						"list_id": this.cardLists[list].id, // Lists id
					}
					if (!isNaN(row)) {
						body["row"] = row;
					}

					console.log(body);

					this.movingCardList = NaN;
					this.movingCardRow = NaN;

					let raw_lists = await fetch("http://" + get_url() + "/card-move/", {
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
				} catch (e) {
					return;
				}

			}
		}
	}
</script>


<template>

	<body @mousemove="">
		<br>
		<!-- <button type="button" @click="">
			bruh
		</button> -->
		<div class="card-list-holder">
			<CardLists v-for="x, i in cardLists" :name="x.name" :items="x.cards" :indent="i"
				:v-bind="currentPositionList" :is-selected-list="currentPositionList == i"
				:moving="!isNaN(movingCardList) && !(movingCardRow == currentPositionRow && currentPositionList == movingCardList)"
				:moving-card="movingCardRow" :selected-card="currentPositionRow" :is-moving-list="movingCardList == i"
				@mouse-entered="mouseEntered" @mouse-left="mouseLeft" @select-card="selectCard">

			</CardLists>
			<div style="margin: auto; margin-left:10pt;">
				<button class="round" @click="makeNewCardList()">
					<div class="button">+</div>
				</button>
			</div>
		</div>
		<Teleport to="body">
			<NewOverlay :show="showModal" :making="this.making" @close="exitModal()" />
		</Teleport>
	</body>
</template>

<style>
	body {
		background-color: #222;
	}

	div.card-list-holder {
		display: flex;
	}

	.button {
		color: black;
	}

	button.round {
		border-radius: 50%;
		width: 51px;
		height: 51px;
		background-color: #04AA6D;
		border: none;
		color: white;
		text-align: center;
		text-decoration: none;
		display: inline;
		font-size: 30px;
	}
</style>