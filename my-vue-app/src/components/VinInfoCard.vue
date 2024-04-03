<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useStore } from '@/store/store';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

const store = useStore();
const cardData = computed(() => store.cardData);

</script>

<template>
  <Card >
    <CardHeader>
      <CardTitle>Vin Details</CardTitle>
      <CardDescription>Vehicle Information</CardDescription>
    </CardHeader>
    <CardContent class="w-[400px]">
        {{cardData}}
    </CardContent>
    <!-- <CardFooter>
      Card Footer
    </CardFooter> -->
  </Card>
  
</template>

<style scoped>

</style>
