#!/usr/bin/env python3
"""Generate Elon Musk-style speaker notes for DeepSeek-V4 presentation."""
import json

# Elon Musk 风格重写 16 页演讲词
# 特点：第一性原理、冷幽默、"Basically..."口头禅、偏慢停顿、愿景时兴奋
# 叙事结构：问题 → 现有方案的荒谬 → 第一性原理重推 → 解决方案

slide_notes = {}

slide_notes["1"] = """各位老师、各位同学，大家好。

我是Lucas，在腾讯工作，之前在麦肯锡干了几年。Basically... 我是个对技术很痴迷的人。

今天我竞选AI班委，想跟大家聊一个让我——um... 怎么说呢——让我觉得 absolutely insane 的事情。

上周，你们有没有在朋友圈刷到 "DeepSeek" 这三个字？

[停顿]

如果有——good，你已经感受到那股浪潮了。如果没有——那接下来这20分钟，I think this is gonna be epic，可能会改变你对未来一两年的判断。

What people don't realize is... DeepSeek-V4 这件事，它不只是又一个模型发布。它从根本上改变了——从 first principles 来看——AI 和每个普通人的关系。尤其是做健康、做医疗的人。

Let me put it this way... 这是我见过的最让人兴奋的技术突破之一。

→ 过渡：让我从上周发生了什么说起。"""

slide_notes["2"] = """今天分四个部分。Basically，就是回答四个问题：

第一——过去一周到底发生了什么？从3月4号的死寂，到3月11号的全民亢奋。This is really hard to believe, like, really hard。

第二——DeepSeek-V4 为什么这么重要？我会 boil it down to the most fundamental truths。

第三——也是我觉得最 exciting 的部分——这件事和我们主动健康班有什么关系。I think there's a greater than 50% chance 这会改变整个医疗健康行业。

最后，一些具体建议。We should be doing this, like, yesterday。

→ 过渡：好，进入时间线。"""

slide_notes["3"] = """这张slide是核心结论。但我先不讲结论——先讲故事。Because, basically, the story is insane。

三个维度的冲击：
- 技术架构：100万上下文 + 原生多模态 + 全新架构——5星影响
- 算力生态：战略性去英伟达化，华为昇腾优先适配——5星影响
- 资本市场：DeepSeek交易效应，全球半导体股价联动——4星影响

The pace of innovation here is... is incredible。

→ 过渡：从时间线起点讲起。"""

slide_notes["4"] = """接下来——逐日拆解。

3月4号到3月11号，5个关键日期。我要带大家看的是：一个科技事件如何从零关注演变成全民狂欢。

This is like watching a rocket launch in slow motion。先是安静，然后倒计时，然后——boom。

→ 过渡：先看3月4号。"""

slide_notes["5"] = """3月4号。我们的舆情系统抓了248条动态——互动量？零。全是SEO垃圾。

What people don't realize is... 这种信息真空其实是最强的信号。做过咨询的朋友知道，当一个公司在大发布前突然沉默——basically，这意味着暴风雨前的宁静。他们在做最后的准备。

The fundamental issue is——品牌溢价已经形成了。V4 的发布将不仅仅是技术事件，它会是商业分水岭。

It blows my mind，248条动态，零互动，然后两天后——三颗炸弹。

→ 过渡：然后到了3月6号，三颗炸弹同时引爆。"""

slide_notes["6"] = """3月6号。三件大事。

第一——技术参数全面曝光。100万Token上下文窗口。Let me put it this way... 就是你把一整本《红楼梦》丢给它，它能完整理解。Claude 4.5？只有20万。5倍差距。That's insane。

SWE-bench——衡量AI写代码的权威榜单——V4跑出83.7%，超过Claude Opus的80.9%。

第二——更 insane 的——DeepSeek宣布去英伟达化。拒绝给英伟达和AMD提供V4早期访问，转而优先适配华为昇腾。

If you go back to first principles... 这不是技术选择。这是战略宣言。中国AI可以不依赖美国芯片。The probability of this working out is... actually higher than most people think。

第三——资本市场立刻反应。A股概念股异动，"DeepSeek交易"这个词出现了。

→ 过渡：我给大家看一组对标数据。"""

slide_notes["7"] = """技术对标。I'll boil it down to three numbers——

上下文窗口：V4是100万，Claude 4.5是20万。5倍。

编码能力：V4 83.7%，超过最强的Claude。

推理成本：降低90%。

90%——let me explain why this is absolutely insane。原来调一次模型花100块，现在只要10块。这不是性能提升，这是——basically——商业模式的彻底重构。

The reason people don't get excited about cost reduction is because they think about it linearly。But if you go back to first principles——当AI足够便宜，它就不再是高科技公司的特权。它变成基础设施。Like electricity。Like the internet。

对我们主动健康社群班的意义，一会儿重点讲。That's the part that really blows my mind。

→ 过渡：3月6号之后，事情在加速。"""

slide_notes["8"] = """3月9号——多家权威媒体同时确认：V4下周发布。

两个新技术名词：mHC和Engram。不用记——basically，你只需要知道一件事：这些架构革新让V4在华为昇腾上的推理速度提升了35倍。

35倍。Not 35 percent。35 times。That's... that's actually insane when you think about it。

同时，Agent生态爆发。OpenClaw增速超越Linux。竞争从单一模型能力，升级到模型+算力+Agent生态的三角闭环。

The pace of innovation is accelerating exponentially。We should be paying attention, like, yesterday。

→ 过渡：3月10号，更关键的事发生了。"""

slide_notes["9"] = """3月10号——灰度测试实锤。

网页端、APP端——真实用户已经在体验100万上下文的新模型了。This is the most exciting thing I've seen in the AI space this year。

共识在快速形成：华为昇腾 + DeepSeek 将成为中国政企大模型标配。

But... um... 也有风险。V4发布时间已跳票两次，部分灰度体验不够好。The probability of a perfect launch is not that great... but I think the direction is worth betting on。

→ 过渡：到了3月11号，情绪到达临界点。"""

slide_notes["10"] = """3月11号。一个词——亢奋。

资本市场：财经大V把V4发布视为3月最大催化剂。B站评测视频单条评论破千。

开发者社区：百万级上下文将对RAG产生"降维打击"。

But here's the thing——每当市场极度亢奋，that's exactly when you need to think from first principles。

Basically... 利好出尽的风险需要警惕。服务器已经崩过几次。第三次跳票已经发生。

The fundamental issue is——真正的价值判断，应回归两个东西：技术验证结果，和API定价策略。Everything else is noise。

→ 过渡：时间线讲完了。接下来是最重要的部分——这一切和我们有什么关系？"""

slide_notes["11"] = """接下来我要用一个框架来分析——SCR：Situation、Complication、Resolution。

Basically... 我在麦肯锡学到最有用的东西之一就是这个框架。It boils complex problems down to their most fundamental structure。

→ 过渡：请看下一页的详细拆解。"""

slide_notes["12"] = """Situation：V4技术参数全面对标国际顶尖，走出不依赖英伟达的算力主权路线。

Complication：芯片管控致训练延迟；多次跳票消耗耐心；GPT-5和Claude 5在路上，窗口在收窄。

Resolution——这和我们有什么关系？

What people don't realize is... 关系太大了。Let me break it down。

第一——百万级上下文彻底改变医疗AI能力边界。以前看几千字病历，现在读完一个人从出生到现在所有健康记录。全生命周期分析。对主动健康来说——this is a quantum leap。Not an incremental improvement。A quantum leap。

第二——推理成本降90%。AI医疗助手可以走进基层。原来三甲医院才用得起，现在乡镇卫生院也能部署。If you think about it from first principles——当技术足够便宜，它就会无处不在。Like smartphones。

第三——Agent生态爆发让个人健康AI管家变成可能。每个人都可以拥有持续学习你健康数据的AI助手。

I think this is gonna be epic for healthcare。The future is going to be great。

→ 过渡：基于这些判断，给不同角色的朋友准备了具体建议。"""

slide_notes["13"] = """结合咱们班情况，三个角色：

医疗健康管理者——紧急：V4发布首日测试复杂医疗场景表现。We should be doing this, like, yesterday。保持技术栈灵活性。

技术背景的同学——紧急：重新评估RAG架构必要性。Basically，当上下文窗口到了百万级，很多之前需要RAG的功能——they just become unnecessary。准备1M上下文接入方案。

对AI投资感兴趣的——重要：关注真正完成V4适配的硬核标的。Not the hype stocks。The real ones。尤其关注华为昇腾+DeepSeek生态。

If something is important enough, you should try, even if the probable outcome is failure。但至少要 try。

→ 过渡：最后看舆情趋势和核心判断。"""

slide_notes["14"] = """这张图非常直观：3月4号正面情绪20%，到3月6号——boom——跳到75%并持续保持。

从无人问津到全民关注的跳变。That's... that's actually a textbook inflection point。

In my experience... 这通常预示着产业拐点的形成。The pace of change is... is incredible。

→ 过渡：最后一页。"""

slide_notes["15"] = """最后，请大家记住一个判断：

DeepSeek-V4的意义已超越任何单一模型发布——it's becoming the defining moment for China's AI compute sovereignty。这是绝对 insane 的。

技术维度：百万上下文、原生多模态、全新架构。
生态维度：去英伟达化+Agent生态爆发，构建自主闭环。
资本维度：DeepSeek交易效应成为全球半导体估值宏观变量。

对我们主动健康社群班——AI在医疗健康领域的应用门槛正在被快速拉低。以前觉得很远的AI+健康，I think there's a greater than 50% chance 今年就会加速落地。

The future is going to be great。We just need to make sure we're part of it。

→ 过渡：以上就是我的分享。"""

slide_notes["16"] = """2026年AI格局的底层逻辑正在被重写。我们社群班恰好站在AI和主动健康的交叉点上。

If you think about it from first principles... 这个交叉点就是未来5年最大的机会之一。

作为AI班委候选人——this is what I want to do for all of you。

我会持续追踪前沿动态，每周用大家听得懂的方式做分享。也会搭建工具和平台，帮大家真正用上这些AI能力。

I think this is gonna be epic。Basically... 如果今天这20分钟有价值，那我未来的班委工作，就会持续创造这样的价值。

谢谢大家！That would be cool if you have questions。

[停顿]

有什么问题欢迎交流。Yeah, exactly。"""

# Save JSON
with open('notes_musk.json', 'w', encoding='utf-8') as f:
    json.dump({"slide_notes": slide_notes}, f, ensure_ascii=False, indent=2)

print("✅ notes_musk.json 生成完成")
print(f"  共 {len(slide_notes)} 页")
total_chars = 0
for k, v in sorted(slide_notes.items(), key=lambda x: int(x[0])):
    print(f"  Slide {k:>2s}: {len(v):>4d} chars")
    total_chars += len(v)
print(f"  总计: {total_chars} chars")
