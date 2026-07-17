<template>
  <div class="min-h-screen relative">
    <Sidebar />
    <main class="ml-64 p-8 relative z-10">
      <div class="mb-8">
        <h2 class="text-3xl font-bold gradient-text">人生档案</h2>
        <p class="text-white/60 mt-2">管理您的个人职业信息，一次填写终身受用</p>
      </div>
      
      <div class="glass-card p-6">
        <el-steps :active="activeStep" align-center class="mb-8">
          <el-step title="基本信息" icon="User" />
          <el-step title="教育背景" icon="GraduationCap" />
          <el-step title="职业履历" icon="Briefcase" />
          <el-step title="技能特长" icon="Star" />
        </el-steps>
        

        <el-form :model="form" ref="formRef" class="space-y-6">
          <div v-if="activeStep === 0" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <el-form-item label="出生年份">
                <el-input-number v-model="form.birth_year" :min="1900" :max="2010" />
              </el-form-item>
              
              <el-form-item label="性别">
                <el-select v-model="form.gender" placeholder="请选择">
                  <el-option label="男" value="男"></el-option>
                  <el-option label="女" value="女"></el-option>
                </el-select>
              </el-form-item>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <el-form-item label="当前行业">
                <el-input v-model="form.current_industry" placeholder="如：互联网、金融、教育"></el-input>
              </el-form-item>
              
              <el-form-item label="当前职位">
                <el-input v-model="form.current_role" placeholder="如：产品经理、前端工程师"></el-input>
              </el-form-item>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <el-form-item label="工作年限">
                <el-input-number v-model="form.work_years" :min="0" :max="50" />
              </el-form-item>
              
              <el-form-item label="薪资区间">
                <el-select v-model="form.salary_range" placeholder="请选择">
                  <el-option label="10k以下" value="10k以下"></el-option>
                  <el-option label="10k-15k" value="10k-15k"></el-option>
                  <el-option label="15k-25k" value="15k-25k"></el-option>
                  <el-option label="25k-40k" value="25k-40k"></el-option>
                  <el-option label="40k以上" value="40k以上"></el-option>
                </el-select>
              </el-form-item>
            </div>
            
            <div>
              <el-form-item label="性格类型">
                <el-select v-model="form.personality_type" placeholder="请选择">
                  <el-option label="INTJ" value="INTJ"></el-option>
                  <el-option label="INTP" value="INTP"></el-option>
                  <el-option label="ENTJ" value="ENTJ"></el-option>
                  <el-option label="ENTP" value="ENTP"></el-option>
                  <el-option label="INFJ" value="INFJ"></el-option>
                  <el-option label="INFP" value="INFP"></el-option>
                  <el-option label="ENFJ" value="ENFJ"></el-option>
                  <el-option label="ENFP" value="ENFP"></el-option>
                  <el-option label="ISTJ" value="ISTJ"></el-option>
                  <el-option label="ISFJ" value="ISFJ"></el-option>
                  <el-option label="ESTJ" value="ESTJ"></el-option>
                  <el-option label="ESFJ" value="ESFJ"></el-option>
                  <el-option label="ISTP" value="ISTP"></el-option>
                  <el-option label="ISFP" value="ISFP"></el-option>
                  <el-option label="ESTP" value="ESTP"></el-option>
                  <el-option label="ESFP" value="ESFP"></el-option>
                </el-select>
              </el-form-item>
            </div>
          </div>
          
          <div v-if="activeStep === 1" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <el-form-item label="最高学历">
                <el-select v-model="form.education" placeholder="请选择">
                  <el-option label="高中/中专" value="高中/中专"></el-option>
                  <el-option label="大专" value="大专"></el-option>
                  <el-option label="本科" value="本科"></el-option>
                  <el-option label="硕士" value="硕士"></el-option>
                  <el-option label="博士" value="博士"></el-option>
                </el-select>
              </el-form-item>
              
              <el-form-item label="专业">
                <el-input v-model="form.major" placeholder="所学专业"></el-input>
              </el-form-item>
              
              <el-form-item label="毕业院校">
                <el-input v-model="form.school" placeholder="毕业院校"></el-input>
              </el-form-item>
            </div>
          </div>
          
          <div v-if="activeStep === 2" class="space-y-6">
            <el-form-item label="工作履历">
              <div class="space-y-3">
                <div v-for="(item, index) in form.career_history" :key="index" class="flex items-center gap-3">
                  <el-input v-model="item.company" placeholder="公司名称" style="width: 180px"></el-input>
                  <el-input v-model="item.role" placeholder="职位" style="width: 120px"></el-input>
                  <el-input v-model="item.period" placeholder="时间范围" style="width: 120px"></el-input>
                  <el-input v-model="item.salary" placeholder="薪资" style="width: 100px"></el-input>
                  <el-button type="danger" size="small" @click="form.career_history.splice(index, 1)">删除</el-button>
                </div>
                <el-button type="primary" size="small" @click="addCareer">添加履历</el-button>
              </div>
            </el-form-item>
          </div>
          
          <div v-if="activeStep === 3" class="space-y-6">
            <el-form-item label="技能矩阵">
              <div class="space-y-3">
                <div v-for="(skill, index) in form.skills" :key="index" class="flex items-center gap-3">
                  <el-input v-model="skill.name" placeholder="技能名称" style="width: 150px"></el-input>
                  <el-select v-model="skill.level" placeholder="熟练程度" style="width: 120px">
                    <el-option label="入门" value="入门"></el-option>
                    <el-option label="熟练" value="熟练"></el-option>
                    <el-option label="精通" value="精通"></el-option>
                  </el-select>
                  <el-input-number v-model="skill.years" :min="0" :max="50" placeholder="年限" style="width: 100px"></el-input-number>
                  <el-button type="danger" size="small" @click="form.skills.splice(index, 1)">删除</el-button>
                </div>
                <el-button type="primary" size="small" @click="addSkill">添加技能</el-button>
              </div>
            </el-form-item>
          </div>
          
          <div class="flex items-center justify-between pt-4">
            <el-button @click="prevStep" :disabled="activeStep === 0">上一步</el-button>
            <div v-if="activeStep < 3">
              <el-button type="primary" @click="handleDraft">保存草稿</el-button>
              <el-button type="primary" @click="nextStep">下一步</el-button>
            </div>
            <div v-else>
              <el-button type="primary" :loading="loading" @click="handleSave">保存档案</el-button>
            </div>
          </div>
        </el-form>
        
        <div class="mt-8 pt-6 border-t border-white/10">
          <h3 class="text-lg font-semibold mb-4">快速导入</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div>
              <h4 class="text-sm font-medium mb-2">上传简历文件</h4>
              <el-upload
                ref="uploadRef"
                :auto-upload="false"
                :limit="1"
                :on-change="handleFileChange"
                :on-exceed="() => ElMessage.warning('只能上传一个文件')"
                accept=".pdf,.docx,.doc,.txt"
              >
                <el-button type="primary">选择文件</el-button>
                <template #tip>
                  <div class="text-xs text-white/50 mt-2">支持 PDF、Word、TXT 格式，最大 5MB</div>
                </template>
              </el-upload>
              <el-button 
                type="primary" 
                :loading="uploadLoading" 
                @click="handleFileUpload"
                class="mt-3"
                :disabled="!uploadFile"
              >
                AI解析上传
              </el-button>
            </div>
            
            <div>
              <h4 class="text-sm font-medium mb-2">粘贴简历文本</h4>
              <el-form :model="resumeForm" ref="resumeFormRef">
                <el-form-item>
                  <el-textarea v-model="resumeForm.resume_text" rows="6" placeholder="请粘贴您的简历文本内容，AI将自动解析填充"></el-textarea>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" :loading="resumeLoading" @click="handleImport">AI解析导入</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <div>
              <h4 class="text-sm font-medium mb-2">链接一键导入</h4>
              <el-form :model="linkForm">
                <el-form-item>
                  <el-input v-model="linkForm.githubUrl" placeholder="GitHub 链接" size="small" />
                </el-form-item>
                <el-form-item>
                  <el-input v-model="linkForm.linkedinUrl" placeholder="LinkedIn 链接" size="small" />
                </el-form-item>
                <el-form-item>
                  <el-input v-model="linkForm.blogUrl" placeholder="博客/技术社区链接" size="small" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" :loading="linkLoading" @click="handleLinkImport">一键导入</el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </div>
        
        <div v-if="versions.length > 1" class="mt-8 pt-6 border-t border-white/10">
          <h3 class="text-lg font-semibold mb-4">版本历史</h3>
          <div class="flex items-center gap-4 mb-4">
            <el-select v-model="compareLeft" placeholder="选择版本 A" style="width: 200px">
              <el-option v-for="v in versions" :key="v.id" :label="`v${v.version} - ${formatDate(v.updated_at || v.created_at)}`" :value="v.version" />
            </el-select>
            <span class="text-white/40">vs</span>
            <el-select v-model="compareRight" placeholder="选择版本 B" style="width: 200px">
              <el-option v-for="v in versions" :key="v.id" :label="`v${v.version} - ${formatDate(v.updated_at || v.created_at)}`" :value="v.version" />
            </el-select>
          </div>
          
          <div v-if="diffFields.length" class="space-y-2">
            <div v-for="field in diffFields" :key="field.key" class="grid grid-cols-3 gap-4 p-3 bg-white/5 rounded-lg">
              <div class="text-sm text-white/60">{{ field.label }}</div>
              <div class="text-sm">
                <span v-if="field.changed" class="text-red-400 line-through">{{ field.left || '-' }}</span>
                <span v-else class="text-white/80">{{ field.left || '-' }}</span>
              </div>
              <div class="text-sm">
                <span v-if="field.changed" class="text-green-400">{{ field.right || '-' }}</span>
                <span v-else class="text-white/80">{{ field.right || '-' }}</span>
              </div>
            </div>
          </div>
          <div v-else class="text-sm text-white/40">两个版本无差异</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { useUserStore } from '../stores/user'
import { profileApi } from '../api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const formRef = ref(null)
const resumeFormRef = ref(null)
const uploadRef = ref(null)
const loading = ref(false)
const resumeLoading = ref(false)
const uploadLoading = ref(false)
const uploadFile = ref(null)
const activeStep = ref(0)
const versions = ref([])
const compareLeft = ref(null)
const compareRight = ref(null)
const linkLoading = ref(false)
const linkForm = reactive({
  githubUrl: '',
  linkedinUrl: '',
  blogUrl: '',
})

const FIELD_LABELS = {
  birth_year: '出生年份',
  gender: '性别',
  education: '最高学历',
  major: '专业',
  school: '毕业院校',
  current_industry: '当前行业',
  current_role: '当前职位',
  work_years: '工作年限',
  salary_range: '薪资区间',
  personality_type: '性格类型',
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const diffFields = computed(() => {
  if (!compareLeft.value || !compareRight.value) return []
  const leftV = versions.value.find(v => v.version === compareLeft.value)
  const rightV = versions.value.find(v => v.version === compareRight.value)
  if (!leftV || !rightV) return []

  return Object.entries(FIELD_LABELS).map(([key, label]) => {
    const left = String(leftV[key] ?? '')
    const right = String(rightV[key] ?? '')
    return { key, label, left, right, changed: left !== right }
  })
})

const form = reactive({
  birth_year: null,
  gender: '',
  education: '',
  major: '',
  school: '',
  skills: [],
  personality_type: '',
  current_industry: '',
  current_role: '',
  work_years: null,
  salary_range: '',
  career_history: [],
})

const resumeForm = reactive({
  resume_text: '',
})

const addSkill = () => {
  form.skills.push({ name: '', level: '熟练', years: 0 })
}

const addCareer = () => {
  form.career_history.push({ company: '', role: '', period: '', salary: '' })
}

const nextStep = () => {
  if (activeStep.value < 3) {
    activeStep.value++
  }
}

const prevStep = () => {
  if (activeStep.value > 0) {
    activeStep.value--
  }
}

const handleDraft = () => {
  localStorage.setItem('profile_draft', JSON.stringify(form))
  ElMessage.success('草稿已保存')
}

const handleSave = async () => {
  loading.value = true
  try {
    await profileApi.update(form)
    await userStore.fetchProfile()
    localStorage.removeItem('profile_draft')
    ElMessage.success('档案保存成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    loading.value = false
  }
}

const handleImport = async () => {
  if (!resumeForm.resume_text.trim()) {
    ElMessage.warning('请先输入简历文本')
    return
  }
  
  resumeLoading.value = true
  try {
    const response = await profileApi.importResume({ resume_text: resumeForm.resume_text })
    applyProfileData(response.data.profile_data)
    ElMessage.success('简历解析成功，请核对并保存')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '解析失败')
  } finally {
    resumeLoading.value = false
  }
}

const handleFileChange = (file) => {
  uploadFile.value = file.raw
}

const handleFileUpload = async () => {
  if (!uploadFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  
  uploadLoading.value = true
  try {
    const response = await profileApi.uploadResume(uploadFile.value)
    applyProfileData(response.data.profile_data)
    ElMessage.success('文件解析成功，请核对并保存')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '文件解析失败')
  } finally {
    uploadLoading.value = false
  }
}

const applyProfileData = (data) => {
  if (data.birth_year !== null) form.birth_year = data.birth_year
  if (data.gender) form.gender = data.gender
  if (data.education) form.education = data.education
  if (data.major) form.major = data.major
  if (data.school) form.school = data.school
  if (data.skills?.length) form.skills = data.skills
  if (data.personality_type) form.personality_type = data.personality_type
  if (data.current_industry) form.current_industry = data.current_industry
  if (data.current_role) form.current_role = data.current_role
  if (data.work_years !== null) form.work_years = data.work_years
  if (data.salary_range) form.salary_range = data.salary_range
  if (data.career_history?.length) form.career_history = data.career_history
}

const handleLinkImport = async () => {
  const sources = []
  if (linkForm.githubUrl.trim()) {
    sources.push({ type: 'github', url: linkForm.githubUrl.trim() })
  }
  if (linkForm.linkedinUrl.trim()) {
    sources.push({ type: 'linkedin', url: linkForm.linkedinUrl.trim() })
  }
  if (linkForm.blogUrl.trim()) {
    sources.push({ type: 'blog', url: linkForm.blogUrl.trim() })
  }
  
  if (sources.length === 0) {
    ElMessage.warning('请至少填写一个链接')
    return
  }
  
  linkLoading.value = true
  try {
    const response = await profileApi.importLinks({ sources })
    applyProfileData(response.data.profile_data)
    ElMessage.success('链接导入成功，请核对并保存')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '导入失败')
  } finally {
    linkLoading.value = false
  }
}

onMounted(async () => {
  await userStore.fetchProfile()
  if (userStore.profile) {
    Object.assign(form, userStore.profile)
  }
  if (!form.skills) form.skills = []
  if (!form.career_history) form.career_history = []
  
  const draft = localStorage.getItem('profile_draft')
  if (draft && !userStore.profile) {
    const draftData = JSON.parse(draft)
    Object.assign(form, draftData)
    ElMessage.info('已加载上次未保存的草稿')
  }
  
  try {
    const res = await profileApi.versions()
    versions.value = res.data
    if (versions.value.length >= 2) {
      compareLeft.value = versions.value[1].version
      compareRight.value = versions.value[0].version
    }
  } catch {}
})

watch(form, (newVal) => {
  localStorage.setItem('profile_draft', JSON.stringify(newVal))
}, { deep: true })
</script>
