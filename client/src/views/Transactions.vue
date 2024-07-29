<template>
  <div>
    <table>
      <thead>
        <tr>
          <!-- <th>UUID</th> -->
          <th>Type</th>
          <th>Start Date</th>
          <th>End Date</th>
          <th>Property ID</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in transactions" :key="transaction.id">
          <!-- <td>{{ transaction.id }}</td> -->
          <td>{{ transaction.type }}</td>
          <td>{{ transaction.start_date }}</td>
          <td>{{ transaction.end_date }}</td>
          <td>{{ transaction.property_id }}</td>
          <td>
            <button @click="showDetails(transaction.id)">Show More Details</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="selectedTransaction">
      <h3>Transaction Details</h3>
      <p>Type: {{ selectedTransaction.type }}</p>
      <p>Start Date: {{ selectedTransaction.start_date }}</p>
      <p>End Date: {{ selectedTransaction.end_date }}</p>
      <!-- Add more fields as necessary -->
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      transactions: [],
      selectedTransaction: null,
    };
  },
  methods: {
    // this method is redundant, should get everything related to transaction then pass into view details 
    async fetchTransactions() {
      const res = await axios.get('/api/transactions');
      this.transactions = res.data;
    },
    async showDetails(id) {
      const res = await axios.get(`'/api/transactions'/${id}`);
      this.selectedTransaction = res.data;
    },
  },
  created() {
    this.fetchTransactions();
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
