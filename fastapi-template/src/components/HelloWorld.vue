<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { InfoIcon } from 'lucide-vue-next'
import VinsCardTable from './VinsCardTable.vue'
import VinInfoCard from './VinInfoCard.vue'

// http://localhost:8000/api/v1/vins


// const vinsData=ref([])

// const getVins = async() => {
//   return fetch('http://localhost:8000/api/v1/vins')
//   .then(response=>response.json())
// }

// onMounted(()=>{
//   getVins().then(data=>{
//     vinsData.value = data
//   })
// })

defineProps<{ msg: string }>()

const count = ref(0)
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <Button type="button" @click="count++">count is {{ count }}</Button>
  </div>
  <div class="flex gap-5">
    <VinsCardTable/>
    <VinInfoCard/>
  </div>

  
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
