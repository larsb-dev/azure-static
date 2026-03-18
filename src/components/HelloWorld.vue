<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import { APP_ENV } from '../env'

const todos = ref([])
const isLoading = ref(true)

const loadTodos = async () => {
    try {
      isLoading.value = true
      const response = await fetch('/api/MyHttpTrigger')
      todos.value = await response.json()
    } catch (error) {
      console.error('Failed to fetch todos:', error)
    } finally {
      isLoading.value = false
    }
}

onMounted(async () => {
  await loadTodos()
})

</script>

<template>
  <h1>Your Todos at {{ APP_ENV ?? 'Unknown' }}</h1>
  <div v-if="isLoading" class="loading-state" role="status" aria-live="polite">
    <span class="spinner" aria-hidden="true"></span>
    <span>Loading todos...</span>
  </div>

  <div v-else>
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        {{ todo.task }}
      </li>
    </ul>
    <button @click="loadTodos">Refresh Todos</button>
  </div>

</template>

<style scoped>
.loading-state {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #d1d5db;
  border-top-color: #2563eb;
  border-radius: 9999px;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
