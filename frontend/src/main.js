import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { 
  Button, 
  Cell, 
  CellGroup,
  Form, 
  Field,
  Toast,
  List,
  PullRefresh,
  NavBar,
  Icon,
  Divider,
  Tag,
  Loading,
  Empty
} from 'vant'
import 'vant/lib/index.css'

const app = createApp(App)
const pinia = createPinia()

// 注册Vant组件
const vantComponents = [
  Button, 
  Cell, 
  CellGroup,
  Form, 
  Field,
  Toast,
  List,
  PullRefresh,
  NavBar,
  Icon,
  Divider,
  Tag,
  Loading,
  Empty
]

vantComponents.forEach(component => {
  app.use(component)
})

app.use(pinia)
app.use(router)
app.mount('#app') 