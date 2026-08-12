<script setup lang="ts">
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
</script>

<template>
  <main class="app">
    <section class="panel">
      <p class="eyebrow">
        Vue Vite
      </p>
      <h1>Application Template</h1>
      <p>API base URL: {{ apiBaseUrl }}</p>
    </section>
  </main>
</template>

