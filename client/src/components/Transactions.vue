<template>
    <div>
      <h1>Real Estate Transactions</h1>
      <ul v-if="transactions.length">
        <li v-for="transaction in transactions" :key="transaction.transaction_id">
          <strong>{{ transaction.type }}</strong>: 
          {{ transaction.start_date }} - {{ transaction.end_date }}
          <br>
          <strong>Property:</strong> {{ transaction.property_name }} ({{ transaction.address }})
          <br>
          <strong>Party:</strong> {{ transaction.party_name }} ({{ transaction.relationship_type }})
        </li>
      </ul>
      <p v-else>No transactions found</p>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  export default {
    setup() {
      const transactions = ref([]);
  
      onMounted(async () => {
        try {
          const response = await axios.get('http://localhost:3000/transactions');
          transactions.value = response.data;
        } catch (error) {
          console.error(error);
        }
      });
  
      return {
        transactions
      };
    }
  };
  </script>
  
  <style scoped>
  /* Add styles here if needed */
  </style>
  