# 参考Java Controller 源码分析草稿

来源：https://www.yuque.com/bbuer/ebdyfe/bvpab2dm6x9bck2y
抓取时间：2026-07-01

---

## PageLayoutController.java 源码分析草稿

- **生成时间:** 2026-06-09
- **来源:** JaCoCo Coverage Report - PageLayoutController.java
- **Controller 类级路径:** /api/bs/ebuilder/designer/layout, /api/{module}/designer/layout
- **Tag:** 设计器布局接口

---

## 一、接口总览（14个端点）

| # | HTTP | 路径 | 描述 | JaCoCo | DB覆盖 | 现有方法 |
|---|------|------|------|--------|--------|---------|
| 1 | GET | /page/info | 根据页面id获取布局信息 | fc ✅ | ✅ | page_designer_layout_info |
| 2 | GET | /theme/info | 获取主题的css内容 | nc ❌ | ❌ | 无 |
| 3 | GET | /getSourceCode | 获取页面源码 | nc ❌ | ❌ | 无 |
| 4 | GET | /getSourceCodeAndId | 获取页面源码和ecodeId | nc ❌ | ❌ | 无 |
| 5 | GET | /list | 根据页面id获取页面信息 | fc ✅ | ✅ | page_designer_layoutList |
| 6 | POST | /save | 布局保存 | fc ✅ | ✅ | page_designer_save |
| 7 | POST | /saveSourceCode | 保存页面源码 | nc ❌ | ❌ | 无 |
| 8 | POST | /uploadThumbnail | 保存缩略图 | fc ✅ | ✅ | page_uploadThumbnail |
| 9 | POST | /lock | 锁定/解锁 | nc ❌ | ✅ | designer_layout_lock |
| 10 | POST | /refTheme | 给页面设置主题 | nc ❌ | ✅ | theme_refTheme |
| 11 | POST | /finishIntro | 完成引导 | fc ✅ | ✅ | finishIntro_designer_layout |
| 12 | POST | /prop/save | 保存用户偏好 | nc ❌ | ❌ | 无 |
| 13 | GET | /var/list | 获取页面变量列表 | nc ❌ | ❌ | 无 |
| 14 | GET | /model/list | 获取页面模型列表 | nc ❌ | ❌ | 无 |

---

## 二、未覆盖接口候选（DB无记录，共7个）

### GET /theme/info — 获取主题的css内容
- **参数:** pageId (Long, @ApiParam)
- **返回:** WeaResult<Map<String, Object>>
- **JaCoCo:** nc（未覆盖）
- **权限:** 无额外权限注解（类级 publicPermission=true）

### GET /getSourceCode — 获取页面源码
- **参数:** pageId (Long), terminalType (TerminalType)
- **返回:** WeaResult<String>
- **JaCoCo:** nc
- **权限:** 无额外权限注解

### GET /getSourceCodeAndId — 获取页面源码和ecodeId
- **参数:** pageId (Long), terminalType (TerminalType)
- **返回:** WeaResult<Map<String, Object>>
- **JaCoCo:** nc
- **权限:** 无额外权限注解

### POST /saveSourceCode — 保存页面源码
- **参数:** pageId (Long, @RequestParam), terminalType (TerminalType, @RequestParam), customConfig (String, @RequestBody)
- **返回:** WeaResult<Boolean>
- **JaCoCo:** nc
- **权限:** @Permission(obj=ObjType.PAGE, opt=OptType.EDIT, id="pageId")

### POST /prop/save — 保存用户偏好
- **参数:** userPreferenceEntityList (List, @RequestBody)
- **返回:** WeaResult<Boolean>
- **JaCoCo:** nc
- **权限:** 无额外权限注解

### GET /var/list — 获取页面变量列表
- **参数:** pageId (Long, @RequestParam)
- **返回:** WeaResult<List<PageVarEntity>>
- **JaCoCo:** nc
- **权限:** 无额外权限注解

### GET /model/list — 获取页面模型列表
- **参数:** pageId (Long, @RequestParam)
- **返回:** WeaResult<List<PageModelEntity>>
- **JaCoCo:** nc
- **权限:** 无额外权限注解

---

## 三、已覆盖接口（DB已有记录，共7个）

- GET /page/info — 已有 page_designer_layout_info
- GET /list — 已有 page_designer_layoutList
- POST /save — 已有 page_designer_save
- POST /uploadThumbnail — 已有 page_uploadThumbnail
- POST /lock — 已有 designer_layout_lock
- POST /refTheme — 已有 theme_refTheme
- POST /finishIntro — 已有 finishIntro_designer_layout

---

## 四、建议测试场景分组

### 场景1: 页面布局查询链路（读操作，3个接口）

**涉及接口:** GET /list → GET /page/info → GET /theme/info

**推断依据:** 三个接口均为GET读操作，共享 pageId 参数；业务语义为"获取页面布局列表 → 获取某页面详细布局 → 获取页面主题样式"，属于页面渲染前的数据准备链路。

**建议:** 合并为一条用例，先获取布局列表确认页面存在，再获取布局详情，最后获取主题信息。

### 场景2: 页面源码读写链路（2个接口）

**涉及接口:** GET /getSourceCode → GET /getSourceCodeAndId

**推断依据:** 两个接口均为GET读操作，共享 pageId + terminalType 参数；业务语义为"获取源码文本"和"获取源码+ecodeId"，属于源码编辑器的数据加载场景。

**建议:** 合并为一条用例，先获取源码确认页面有源码，再获取源码和ecodeId验证数据完整性。

### 场景3: 页面源码保存（独立写操作，1个接口）

**涉及接口:** POST /saveSourceCode

**推断依据:** 独立的写操作，需要 pageId + terminalType + customConfig (JSON body)。需要先有页面和布局数据才能保存源码。有 @Permission(EDIT) 权限要求。

**建议:** 独立用例，前置先调用 /list 获取布局信息，再调用 /saveSourceCode 保存。

### 场景4: 页面变量与模型查询（读操作，2个接口）

**涉及接口:** GET /var/list → GET /model/list

**推断依据:** 两个接口均为GET读操作，共享 pageId 参数；业务语义为"获取页面变量列表"和"获取页面模型列表"，属于页面配置信息查询。

**建议:** 合并为一条用例。

### 场景5: 保存用户偏好（独立写操作，1个接口）

**涉及接口:** POST /prop/save

**推断依据:** 独立写操作，接收 List<UserPreferenceEntity> 作为 body。参数结构较特殊（实体列表），与其它接口无直接依赖关系。

**建议:** 独立用例。需要了解 UserPreferenceEntity 的结构才能构造 payload。

---

## 五、参数来源特殊接口

| 接口 | 特殊参数 | 说明 |
|------|---------|------|
| POST /saveSourceCode | customConfig (@RequestBody) | JSON 字符串，包含 sourceCode 和 ebCodeFileTypes |
| POST /prop/save | List<UserPreferenceEntity> (@RequestBody) | 实体列表，需了解实体字段结构 |
| GET /getSourceCode | terminalType (TerminalType枚举) | 需确认枚举值（如 PC/MOBILE） |
| GET /getSourceCodeAndId | terminalType (TerminalType枚举) | 同上 |

---

## 六、备注

- /lock 和 /refTheme 虽然 JaCoCo 显示未覆盖，但 DB 中已有接口方法记录，本次不作为新增候选
- /saveSourceCode 与已有 /save 的区别：/save 保存布局JSON，/saveSourceCode 保存源码配置
- 类级 @WeaPermission(publicPermission=true) 表示所有接口默认公开访问，但个别接口有 @Permission 注解做细粒度权限控制

## 🔗 自动关联索引

<!-- AUTO-LINK-INDEX:START -->
- [[capture-抓包底座使用指引]] — AI测试主题关联
- [[通过AI+SKILL维护用例的测试记录]] — AI测试主题关联
- [[通过AI+SKILL编写自动化测试用例记录]] — AI测试主题关联
- [[通过Claude Code和接口用例SKILL高效编写和维护接口自动化用例]] — AI测试主题关联
- [[SKILLS问题记录]] — AI测试主题关联
- [[接口自动化SKILL的提效记录]] — AI测试主题关联
- [[通过AI+SKILL编写接口用例的提效记录-表格]] — AI测试主题关联
- [[通过AI实现全流程的接口自动化]] — AI测试主题关联
<!-- AUTO-LINK-INDEX:END -->
