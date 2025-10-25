# 照片展示系统使用说明

## 概述
这个照片展示系统现在支持通过配置文件轻松更新，无需修改代码即可调整各种参数。

## 配置文件位置
`_data/photo_config.yml`

## 如何添加新照片

### 1. 添加数字照片
在 `_data/photo.yml` 中添加新的照片条目：
```yaml
- image: "/assets/img/photo/digital/新照片.jpg"
```

### 2. 添加胶片照片
在 `_data/film.yml` 中添加新的照片条目：
```yaml
- image: "/assets/img/photo/film/新照片.jpg"
```

### 3. 照片文件放置
- 数字照片：放在 `assets/img/photo/digital/` 目录
- 胶片照片：放在 `assets/img/photo/film/` 目录

## 配置参数说明

### 动画设置
```yaml
animation:
  base_delay: 0.1        # 第一张照片的延迟时间（秒）
  delay_increment: 0.1   # 每张照片的延迟增量（秒）
  max_delay: 1.6         # 最大延迟时间（秒）
  fade_duration: 0.6     # 淡入动画持续时间（秒）
```

### 照片尺寸设置
```yaml
sizing:
  base_size_min: 200     # 照片最小尺寸（像素）
  base_size_max: 300     # 照片最大尺寸（像素）
  scale_factor: 0.25     # 缩放因子（原始尺寸的倍数）
```

### 布局设置
```yaml
layout:
  margin: 50             # 照片间距（像素）
  padding: 30           # 容器内边距（像素）
  rotation_range: 10     # 旋转角度范围（度）
```

### 弹窗设置
```yaml
modal:
  background_opacity: 0.9    # 背景透明度（0-1）
  animation_duration: 0.3    # 弹窗动画持续时间（秒）
  max_width_percent: 90      # 弹窗最大宽度百分比
  max_height_percent: 90     # 弹窗最大高度百分比
```

## 常见调整场景

### 1. 添加更多照片后调整动画延迟
如果添加了很多照片，可以调整：
- `delay_increment`: 减小增量让动画更快
- `max_delay`: 增加最大延迟时间

### 2. 调整照片大小
- `base_size_min` 和 `base_size_max`: 调整照片显示尺寸范围
- `scale_factor`: 调整整体缩放比例

### 3. 调整布局密度
- `margin`: 调整照片间距
- `padding`: 调整容器边距

### 4. 调整弹窗效果
- `background_opacity`: 调整背景透明度
- `max_width_percent` 和 `max_height_percent`: 调整弹窗大小

## 注意事项
1. 修改配置文件后需要重新启动Jekyll服务器
2. 照片文件名建议使用英文和数字，避免特殊字符
3. 建议照片尺寸不要过大，影响加载速度
4. 动画延迟会自动根据照片数量计算，无需手动设置每张照片的延迟

## 示例：添加10张新照片
1. 将照片文件放入对应目录
2. 在 `photo.yml` 或 `film.yml` 中添加10个条目
3. 如果需要，调整 `max_delay` 为更大的值（如2.0）
4. 重启Jekyll服务器查看效果

