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
import { MapCard } from 'vue-map-card'
import { ZapIcon } from 'lucide-vue-next'

const store = useStore();
const cardData = computed(() => store.cardData);
const vehicledata = computed(() => cardData.value?.vehicle_data);
const location = computed(() => cardData.value?.location);

</script>

<template>
  <Card >
    <CardHeader>
      <CardTitle>Car Location</CardTitle>
      <CardDescription>Vehicle Information</CardDescription>
    </CardHeader>
    <CardContent class="w-[400px]">
      <div class="text-xl font-bold flex justify-center ">
        <img :src="'https://flagcdn.com/' + location?.country_code + '.svg'" class="h-6 "/>
      </div>
      <div class="text-xl font-bold ">
        {{ location?.city }}, {{ location?.country }}
      </div>
      <p class="text-xs text-muted-foreground ">
        ({{ vehicledata?.latitude }}, {{ vehicledata?.longitude }})
      </p>
      <div class="flex justify-center text-2xl font-bold py-2">
        <ZapIcon class="pt-2 text-green-500" size="25"/> {{ parseInt(vehicledata?.remaining_electrical_range) }} miles remaining
      </div>


      <!-- {{ vehicledata }} -->
      
      <MapCard 
      :city="location?.city"
      :country="location?.country"
      />
    </CardContent>
    <!-- <CardFooter>
      Card Footer
    </CardFooter> -->
  </Card>
  
</template>

<style scoped>

</style>
