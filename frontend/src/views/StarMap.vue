<template>
  <div class="min-h-screen">
    <Sidebar />
    <main class="ml-64 p-8">
      <div class="mb-8">
        <h2 class="text-2xl font-bold">人生星图</h2>
        <p class="text-white/60 mt-1">以星空方式呈现您的人生蓝图，每个里程碑都是一颗星</p>
      </div>
      
      <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
        <div v-if="loading" class="flex items-center justify-center py-20">
          <el-loading :text="'正在绘制星图...'" />
        </div>
        
        <div v-else-if="data.nodes.length" class="relative">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-2">
                <span class="w-4 h-4 rounded-full bg-star-cyan"></span>
                <span class="text-sm text-white/60">短期目标</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-4 h-4 rounded-full bg-star-primary"></span>
                <span class="text-sm text-white/60">中期目标</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-4 h-4 rounded-full bg-star-pink"></span>
                <span class="text-sm text-white/60">长期目标</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <el-button size="small" @click="playAnimation">🎬 播放路径动画</el-button>
              <el-button size="small" @click="resetView">🔄 重置视图</el-button>
              <el-switch v-model="draggable" active-text="可拖拽" inactive-text="固定" />
            </div>
          </div>
          
          <div ref="chartRef" class="w-full h-[600px]"></div>
          
          <div v-if="selectedNode" class="mt-4 p-4 bg-white/5 rounded-lg">
            <div class="flex items-start justify-between">
              <div>
                <h4 class="font-medium">{{ selectedNode.name }}</h4>
                <p class="text-sm text-white/60 mt-1">概率：{{ Math.round(selectedNode.probability * 100) }}%</p>
                <p class="text-sm text-white/60">类别：{{ selectedNode.category }}</p>
                <p v-if="selectedNode.metrics?.target_role" class="text-sm text-white/60">目标职位：{{ selectedNode.metrics.target_role }}</p>
                <p v-if="selectedNode.metrics?.target_salary" class="text-sm text-white/60">目标薪资：{{ selectedNode.metrics.target_salary }}</p>
              </div>
              <el-button size="small" @click="selectedNode = null">关闭</el-button>
            </div>
          </div>
          
          <div class="mt-4 p-4 bg-white/5 rounded-lg">
            <h4 class="text-sm font-medium mb-2">图例说明</h4>
            <p class="text-xs text-white/60">节点大小代表重要性，亮度代表达成概率；实线为主推荐路径，虚线为备选路径。点击节点查看详情，开启拖拽可自由调整星图布局。</p>
          </div>
        </div>
        
        <div v-else class="text-center py-20">
          <p class="text-6xl mb-4">🌌</p>
          <p class="text-xl">星图为空</p>
          <p class="text-white/60 mt-2">生成职业规划后，您的人生星图将在这里展现</p>
          <el-button type="primary" @click="$router.push('/plan')" class="mt-4">去生成规划</el-button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import Sidebar from '../components/Sidebar.vue'
import { starmapApi } from '../api'

const chartRef = ref(null)
const loading = ref(false)
const data = ref({ nodes: [], edges: [] })
const draggable = ref(false)
const selectedNode = ref(null)
let chart = null
let animationInterval = null

const colorMap = {
  short_term: '#a8edea',
  mid_term: '#667eea',
  long_term: '#fed6e3',
  skill: '#a8edea',
  career: '#667eea',
  income: '#fed6e3',
}

const initChart = () => {
  if (!chartRef.value) return
  
  chart?.dispose()
  chart = echarts.init(chartRef.value)
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(36, 36, 62, 0.9)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      textStyle: { color: '#fff' },
      formatter: (params) => {
        if (params.dataType === 'node') {
          const node = params.data
          return `<div style="font-weight:bold;margin-bottom:8px;">${node.name}</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.6);">
              概率: ${Math.round(node.probability * 100)}%<br/>
              类别: ${node.category}<br/>
              目标: ${node.metrics?.target_role || '-'}
            </div>`
        }
        return ''
      }
    },
    series: [{
      type: 'graph',
      layout: 'none',
      coordinateSystem: undefined,
      roam: true,
      draggable: draggable.value,
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 4 },
        itemStyle: { shadowBlur: 40 }
      },
      data: data.value.nodes.map(node => ({
        id: node.id,
        name: node.title,
        x: node.x * 7,
        y: (100 - node.y) * 5.5,
        symbolSize: node.size * 3,
        itemStyle: {
          color: node.color,
          shadowBlur: node.probability * 30,
          shadowColor: node.color,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'bottom',
          distance: 10,
          fontSize: 11,
          color: '#fff',
          formatter: (params) => `${params.name}\n${params.data.probability * 100}%`
        },
        category: node.category,
        probability: node.probability,
        metrics: node.metrics
      })),
      links: data.value.edges.map(edge => ({
        source: edge.source,
        target: edge.target,
        lineStyle: {
          color: edge.path_type === 'main' ? '#667eea' : '#a8edea',
          width: edge.path_type === 'main' ? 3 : 1,
          type: edge.path_type === 'main' ? 'solid' : 'dashed',
          opacity: 0.6,
          curveness: 0.1
        }
      })),
      animationDuration: 1500,
      animationEasingUpdate: 'quinticInOut'
    }]
  }
  
  chart.setOption(option)
  
  chart.on('click', (params) => {
    if (params.dataType === 'node') {
      selectedNode.value = params.data
    }
  })
  
  chart.on('mouseout', () => {
    if (chart) {
      chart.dispatchAction({ type: 'downplay' })
    }
  })
}

const playAnimation = () => {
  if (!chart || !data.value.edges.length) return
  
  const mainEdges = data.value.edges.filter(e => e.path_type === 'main')
  let currentIndex = 0
  
  if (animationInterval) clearInterval(animationInterval)
  
  animationInterval = setInterval(() => {
    if (currentIndex >= mainEdges.length) {
      clearInterval(animationInterval)
      chart.dispatchAction({ type: 'highlight', seriesIndex: 0 })
      return
    }
    
    const edge = mainEdges[currentIndex]
    chart.dispatchAction({
      type: 'highlight',
      seriesIndex: 0,
      dataIndex: data.value.nodes.findIndex(n => n.id === edge.source)
    })
    chart.dispatchAction({
      type: 'highlight',
      seriesIndex: 0,
      dataIndex: data.value.nodes.findIndex(n => n.id === edge.target)
    })
    
    currentIndex++
  }, 800)
}

const resetView = () => {
  if (chart) {
    chart.dispatchAction({ type: 'dataZoom', start: 0, end: 100 })
    chart.dispatchAction({ type: 'downplay', seriesIndex: 0 })
  }
  selectedNode.value = null
}

const fetchData = async () => {
  loading.value = true
  try {
    const response = await starmapApi.get()
    data.value = response.data
  } catch {} finally {
    loading.value = false
  }
}

const handleResize = () => {
  chart?.resize()
}

onMounted(async () => {
  await fetchData()
  setTimeout(initChart, 100)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
  if (animationInterval) clearInterval(animationInterval)
})

watch(draggable, () => {
  initChart()
})

watch(() => data.value.nodes.length, () => {
  initChart()
})
</script>
