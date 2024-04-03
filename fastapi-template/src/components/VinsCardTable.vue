<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Button } from '@/components/ui/button'
import { useStore } from '@/store/store';
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
import { InfoIcon, ChevronRight } from 'lucide-vue-next'

// http://localhost:8000/api/v1/vins


const vinsData=ref([])

const getVins = async() => {
  return fetch('http://localhost:8000/api/v1/vins')
  .then(response=>response.json())
}

onMounted(()=>{
  getVins().then(data=>{
    vinsData.value = data
  })
})

const fetchVinData = async (vin: string) => {
      try {
        await useStore().fetchData(vin);
        console.log(`Data fetched for VIN ${vin}`);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
};

</script>

<template>
  <Card >
    <CardHeader>
      <CardTitle>VINs</CardTitle>
      <CardDescription>Vehicle Identification</CardDescription>
    </CardHeader>
    <CardContent>
      <Table>
        <!-- <TableCaption>.</TableCaption> -->
        <TableHeader>
          <TableRow>
            <TableHead class="w-[100px]">
              VIN
            </TableHead>
            <TableHead class="text-center">
              Options
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="vin in vinsData" :key="vin">
            <TableCell class="font-medium">
              {{ vin }}
            </TableCell>
            <TableCell class="text-right">
              <Button @click="fetchVinData(vin)" variant="outline" class="bg-card" title="See details"><ChevronRight size="25"/></Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </CardContent>
    <!-- <CardFooter>
      Card Footer
    </CardFooter> -->
  </Card>
  
</template>

<style scoped>

</style>
