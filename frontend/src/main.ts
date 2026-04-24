import { createApp } from 'vue'
import {
  ElAlert,
  ElButton,
  ElCard,
  ElCheckbox,
  ElDivider,
  ElEmpty,
  ElForm,
  ElFormItem,
  ElInput,
  ElResult,
  ElSkeleton,
  ElTable,
  ElTableColumn,
  ElTag,
  ElTabs,
  ElTabPane,
} from 'element-plus'
import 'element-plus/es/components/alert/style/css'
import 'element-plus/es/components/button/style/css'
import 'element-plus/es/components/card/style/css'
import 'element-plus/es/components/checkbox/style/css'
import 'element-plus/es/components/divider/style/css'
import 'element-plus/es/components/empty/style/css'
import 'element-plus/es/components/form/style/css'
import 'element-plus/es/components/form-item/style/css'
import 'element-plus/es/components/input/style/css'
import 'element-plus/es/components/message/style/css'
import 'element-plus/es/components/result/style/css'
import 'element-plus/es/components/skeleton/style/css'
import 'element-plus/es/components/tag/style/css'
import 'element-plus/es/components/table/style/css'
import 'element-plus/es/components/tabs/style/css'
import './styles/index.css'
import './styles/element-mobile-dark.css'
import App from './App.vue'
import router from './router'
import { pinia } from './stores'

const app = createApp(App)

app.component('ElAlert', ElAlert)
app.component('ElButton', ElButton)
app.component('ElCard', ElCard)
app.component('ElCheckbox', ElCheckbox)
app.component('ElDivider', ElDivider)
app.component('ElEmpty', ElEmpty)
app.component('ElForm', ElForm)
app.component('ElFormItem', ElFormItem)
app.component('ElInput', ElInput)
app.component('ElResult', ElResult)
app.component('ElSkeleton', ElSkeleton)
app.component('ElTable', ElTable)
app.component('ElTableColumn', ElTableColumn)
app.component('ElTag', ElTag)
app.component('ElTabs', ElTabs)
app.component('ElTabPane', ElTabPane)

app.use(pinia).use(router).mount('#app')
