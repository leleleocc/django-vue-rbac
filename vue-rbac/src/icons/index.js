import SvgIcon from '@/components/SvgIcon'

const svgRequired = require.context('./svg', false, /\.svg$/)
svgRequired.keys().forEach((item) => svgRequired(item))

//将图标-》组件
export default (app) => {
  app.component('svg-icon', SvgIcon)
}
