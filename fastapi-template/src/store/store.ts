import { defineStore } from 'pinia';

interface RootState {
  cardData: any; // Replace 'any' with the type of your card data
}

export const useStore = defineStore({
  id: 'store',
  state: (): RootState => ({
    cardData: null
  }),
  actions: {
    async fetchData(vin: string) {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/vehicle/${vin}/last`);
        const data = await response.json();
        this.cardData = data;
      } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
      }
    }
  }
});