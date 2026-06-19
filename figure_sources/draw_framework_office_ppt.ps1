$ErrorActionPreference = "Stop"

$outDir = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($outDir)) {
    $outDir = (Get-Location).Path
}
$pptxPath = Join-Path $outDir "图1论文框架图_OfficePPT_0603.pptx"
$previewPath = Join-Path $outDir "图1论文框架图_OfficePPT_0603.png"

function RgbColor([int]$r, [int]$g, [int]$b) {
    return $r + ($g * 256) + ($b * 65536)
}

function Set-Text($shape, [string]$text, [int]$size, [int]$color, [bool]$bold = $false, [int]$align = 1) {
    $shape.TextFrame2.TextRange.Text = $text
    $shape.TextFrame2.WordWrap = -1
    $shape.TextFrame2.MarginLeft = 6
    $shape.TextFrame2.MarginRight = 6
    $shape.TextFrame2.MarginTop = 3
    $shape.TextFrame2.MarginBottom = 3
    $shape.TextFrame2.VerticalAnchor = 1
    $shape.TextFrame2.TextRange.Font.NameFarEast = "Microsoft YaHei"
    $shape.TextFrame2.TextRange.Font.Name = "Arial"
    $shape.TextFrame2.TextRange.Font.Size = $size
    $shape.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = $color
    $shape.TextFrame2.TextRange.Font.Bold = [int]$bold
    $shape.TextFrame2.TextRange.ParagraphFormat.Alignment = $align
}

function Add-RoundBox($slide, [double]$x, [double]$y, [double]$w, [double]$h,
    [int]$fill, [int]$line, [double]$weight = 1.2, [string]$dash = "solid") {
    $shape = $slide.Shapes.AddShape(5, $x, $y, $w, $h)
    $shape.Fill.ForeColor.RGB = $fill
    $shape.Line.ForeColor.RGB = $line
    $shape.Line.Weight = $weight
    if ($dash -eq "dash") { $shape.Line.DashStyle = 4 }
    return $shape
}

function Add-TextBox($slide, [double]$x, [double]$y, [double]$w, [double]$h,
    [string]$text, [int]$size, [int]$color, [bool]$bold = $false, [int]$align = 1) {
    $shape = $slide.Shapes.AddTextbox(1, $x, $y, $w, $h)
    Set-Text $shape $text $size $color $bold $align
    return $shape
}

function Add-Arrow($slide, [double]$x1, [double]$y1, [double]$x2, [double]$y2,
    [int]$color, [double]$weight = 2.0, [bool]$dash = $false) {
    $line = $slide.Shapes.AddConnector(1, $x1, $y1, $x2, $y2)
    $line.Line.ForeColor.RGB = $color
    $line.Line.Weight = $weight
    $line.Line.EndArrowheadStyle = 3
    if ($dash) { $line.Line.DashStyle = 4 }
    return $line
}

function Add-Card($slide, [double]$x, [double]$y, [double]$w, [double]$h,
    [string]$title, [string]$body, [int]$accent, [int]$border, [int]$fill,
    [string]$icon = "") {
    $box = Add-RoundBox $slide $x $y $w $h $fill $border 1.1
    $box.Line.Weight = 1.1
    $bar = $slide.Shapes.AddShape(1, $x + 8, $y + 6, $w - 16, 4)
    $bar.Fill.ForeColor.RGB = $accent
    $bar.Line.Visible = 0
    if ($icon.Length -gt 0) {
        $ico = Add-TextBox $slide ($x + 8) ($y + 28) 52 55 $icon 28 $accent $false 2
        $ico.TextFrame2.VerticalAnchor = 3
        $textX = $x + 66
        $textW = $w - 76
    } else {
        $textX = $x + 12
        $textW = $w - 24
    }
    Add-TextBox $slide $textX ($y + 20) $textW 20 $title 13 $accent $true 1 | Out-Null
    Add-TextBox $slide $textX ($y + 44) $textW ($h - 48) $body 8 (RgbColor 20 20 20) $false 1 | Out-Null
    return $box
}

function Add-CloudPlatform($slide, [double]$x, [double]$y, [double]$w, [double]$h, [int]$blue, [int]$soft) {
    $base = Add-RoundBox $slide ($x + 35) ($y + 40) ($w - 70) ($h - 55) $soft $blue 2.2
    $parts = @(
        @(($x + 35), ($y + 38), 72, 55),
        @(($x + 88), ($y + 8), 90, 76),
        @(($x + 158), ($y + 22), 82, 62),
        @(($x + 14), ($y + 57), 66, 44),
        @(($x + 218), ($y + 58), 56, 42)
    )
    foreach ($p in $parts) {
        $o = $slide.Shapes.AddShape(9, $p[0], $p[1], $p[2], $p[3])
        $o.Fill.ForeColor.RGB = $soft
        $o.Line.ForeColor.RGB = $blue
        $o.Line.Weight = 2.2
    }
    $base.ZOrder(1)
    Add-TextBox $slide ($x + 74) ($y + 38) 130 20 "Token 平台 / 聚合器" 11 (RgbColor 0 43 125) $true 2 | Out-Null
    $server = $slide.Shapes.AddShape(1, $x + 90, $y + 66, 45, 42)
    $server.Fill.ForeColor.RGB = (RgbColor 10 65 110)
    $server.Line.ForeColor.RGB = (RgbColor 10 65 110)
    for ($i = 0; $i -lt 3; $i++) {
        $slot = $slide.Shapes.AddShape(1, $x + 98, $y + 72 + 10 * $i, 28, 4)
        $slot.Fill.ForeColor.RGB = (RgbColor 64 154 196)
        $slot.Line.Visible = 0
    }
    $screen = $slide.Shapes.AddShape(5, $x + 148, $y + 66, 70, 42)
    $screen.Fill.ForeColor.RGB = (RgbColor 246 250 255)
    $screen.Line.ForeColor.RGB = $blue
    Add-TextBox $slide ($x + 154) ($y + 72) 58 25 "价格`n需求`nQoS" 8 (RgbColor 0 43 125) $true 2 | Out-Null
    $db = $slide.Shapes.AddShape(7, $x + 224, $y + 70, 34, 38)
    $db.Fill.ForeColor.RGB = (RgbColor 65 155 210)
    $db.Line.ForeColor.RGB = $blue
}

function Add-Metric($slide, [double]$x, [double]$y, [double]$w, [double]$h,
    [string]$label, [string]$value, [int]$valueColor, [int]$border) {
    Add-RoundBox $slide $x $y $w $h (RgbColor 250 255 251) $border 1.1 | Out-Null
    Add-TextBox $slide ($x + 4) ($y + 7) ($w - 8) 18 $label 8 (RgbColor 20 20 20) $false 2 | Out-Null
    Add-TextBox $slide ($x + 4) ($y + 28) ($w - 8) 20 $value 12 $valueColor $true 2 | Out-Null
}

function Add-LineChart($slide, [double]$x, [double]$y, [double]$w, [double]$h,
    [int]$blue, [int]$red) {
    $plotX = $x + 22
    $plotY = $y + 20
    $plotW = $w - 82
    $plotH = $h - 36
    Add-TextBox $slide ($x + 6) ($y + 2) ($w - 12) 16 "TTFT 随并发请求变化（示意）" 8 (RgbColor 20 20 20) $false 2 | Out-Null
    $axis1 = $slide.Shapes.AddConnector(1, $plotX, $plotY + $plotH, $plotX + $plotW, $plotY + $plotH)
    $axis2 = $slide.Shapes.AddConnector(1, $plotX, $plotY, $plotX, $plotY + $plotH)
    foreach ($a in @($axis1, $axis2)) {
        $a.Line.ForeColor.RGB = (RgbColor 80 80 80)
        $a.Line.Weight = 1
    }
    $pts = @(
        @(($plotX + 6), ($plotY + $plotH - 10)),
        @(($plotX + 34), ($plotY + $plotH - 15)),
        @(($plotX + 65), ($plotY + $plotH - 24)),
        @(($plotX + 100), ($plotY + $plotH - 38)),
        @(($plotX + 137), ($plotY + $plotH - 58)),
        @(($plotX + 174), ($plotY + 12))
    )
    for ($i = 0; $i -lt $pts.Count - 1; $i++) {
        $seg = $slide.Shapes.AddConnector(1, $pts[$i][0], $pts[$i][1], $pts[$i+1][0], $pts[$i+1][1])
        $seg.Line.ForeColor.RGB = $blue
        $seg.Line.Weight = 1.8
    }
    foreach ($p in $pts) {
        $dot = $slide.Shapes.AddShape(9, $p[0] - 3, $p[1] - 3, 6, 6)
        $dot.Fill.ForeColor.RGB = (RgbColor 255 255 255)
        $dot.Line.ForeColor.RGB = $blue
        $dot.Line.Weight = 1.2
    }
    $thr = $slide.Shapes.AddConnector(1, $plotX + 130, $plotY, $plotX + 130, $plotY + $plotH)
    $thr.Line.ForeColor.RGB = $red
    $thr.Line.DashStyle = 4
    Add-TextBox $slide ($plotX + 136) ($plotY + $plotH - 18) 42 14 "高并发区" 7 $red $true 1 | Out-Null
    Add-TextBox $slide ($plotX + 48) ($plotY + $plotH + 1) 92 12 "并发请求数" 7 (RgbColor 20 20 20) $false 2 | Out-Null
}

$ppt = $null
$prs = $null
try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $ppt.Visible = -1
    $prs = $ppt.Presentations.Add()
    $prs.PageSetup.SlideWidth = 960
    $prs.PageSetup.SlideHeight = 540
    $slide = $prs.Slides.Add(1, 12)
    $slide.Background.Fill.ForeColor.RGB = (RgbColor 255 255 255)

    $black = RgbColor 0 0 0
    $navy = RgbColor 0 43 125
    $blue = RgbColor 0 92 220
    $blueSoft = RgbColor 238 247 255
    $green = RgbColor 13 117 46
    $greenSoft = RgbColor 239 249 241
    $orange = RgbColor 244 91 24
    $orangeSoft = RgbColor 255 250 239
    $purple = RgbColor 103 58 183
    $purpleSoft = RgbColor 249 246 255
    $red = RgbColor 214 33 33
    $gray = RgbColor 80 80 80
    $lightGray = RgbColor 248 249 251

    Add-TextBox $slide 20 6 920 34 "固定平均标价约束下 Token 服务跨时段定价" 28 $black $true 2 | Out-Null
    Add-TextBox $slide 20 42 920 20 "方法框架、仿真求解与单 GPU 拥挤验证" 15 $black $false 2 | Out-Null

    $leftPanel = Add-RoundBox $slide 10 78 275 370 (RgbColor 255 255 255) $orange 1.4 "dash"
    $midPanel = Add-RoundBox $slide 300 78 360 370 (RgbColor 255 255 255) $blue 1.4 "dash"
    $rightPanel = Add-RoundBox $slide 675 78 275 370 (RgbColor 255 255 255) $purple 1.4 "dash"

    $leftHead = Add-RoundBox $slide 18 86 259 28 $orangeSoft $orange 1.0
    Set-Text $leftHead "方法动机" 16 $orange $true 2
    $midHead = Add-RoundBox $slide 308 86 344 28 $blueSoft $blue 1.0
    Set-Text $midHead "理论模型与求解" 16 $black $true 2
    $rightHead = Add-RoundBox $slide 683 86 259 28 $purpleSoft $purple 1.0
    Set-Text $rightHead "结果与验证" 16 $black $true 2

    $cardA = Add-Card $slide 18 124 259 92 "A. 研究背景" "• 电力需求响应启发`n• 推理请求存在时段负载波动`n• 过载导致 TTFT↑、超时↑、有效吞吐↓" $red $red (RgbColor 255 253 253) ""
    Add-Arrow $slide 147 219 147 232 (RgbColor 87 107 125) 2.4 | Out-Null
    $cardB = Add-Card $slide 18 236 259 92 "B. 建模目标" "• 固定平均标价约束下发布时段价格`n• 迁移弹性需求，缓解峰时拥挤`n• 同时提升利润与 QoS" $orange $orange (RgbColor 255 253 248) ""
    Add-Arrow $slide 147 331 147 346 (RgbColor 87 107 125) 2.4 | Out-Null
    $cardC = Add-Card $slide 18 350 259 88 "C. 核心思路" "• 单平台领导者--跟随者结构`n• 价格信号协调跨时段需求迁移`n• QoS 退化进入平台目标" $purple $purple (RgbColor 253 251 255) ""

    Add-CloudPlatform $slide 342 122 245 112 $blue (RgbColor 239 248 255)
    $toolY = 248
    $tools = @(
        @("数据管理", "D_t, u_t"),
        @("需求预测", "R_t + F_t"),
        @("约束优化", "mean(p)=p̄"),
        @("监测诊断", "QoS / SLA")
    )
    for ($i = 0; $i -lt 4; $i++) {
        $x = 314 + 84 * $i
        $box = Add-RoundBox $slide $x $toolY 74 54 (RgbColor 248 252 255) $blue 1.0
        Set-Text $box ($tools[$i][0] + "`n" + $tools[$i][1]) 8 (RgbColor 0 43 125) $false 2
    }
    Add-Arrow $slide 480 302 480 330 $gray 2.0 | Out-Null

    $game = Add-RoundBox $slide 330 330 300 84 (RgbColor 253 254 255) $blue 1.3 "dash"
    Add-TextBox $slide 342 336 278 16 "动态定价博弈（领导者--跟随者）" 11 $navy $true 2 | Out-Null
    $steps = @(
        @("需求响应", "D_t"),
        @("价格决策", "p_t"),
        @("QoS 代理", "q(u_t)"),
        @("目标函数", "Π / Welfare")
    )
    for ($i = 0; $i -lt 4; $i++) {
        $sx = 350 + 68 * $i
        $sbox = Add-RoundBox $slide $sx 362 54 40 (RgbColor 255 255 255) (RgbColor 210 220 230) 0.8
        Set-Text $sbox ($steps[$i][0] + "`n" + $steps[$i][1]) 7 $black $false 2
        if ($i -lt 3) {
            Add-Arrow $slide ($sx + 55) 382 ($sx + 66) 382 $gray 1.4 | Out-Null
        }
    }
    Add-Arrow $slide 626 374 650 374 $orange 2.0 | Out-Null
    Add-TextBox $slide 634 342 40 32 "负载`n供给" 8 $black $false 2 | Out-Null
    Add-Arrow $slide 309 374 286 374 $blue 2.0 | Out-Null
    Add-TextBox $slide 258 342 40 32 "价格`n信号" 8 $black $false 2 | Out-Null

    $feedback = Add-RoundBox $slide 350 422 260 42 (RgbColor 253 250 255) $purple 1.2 "dash"
    Add-TextBox $slide 365 425 230 13 "迭代反馈（响应与策略更新）" 9 $purple $true 2 | Out-Null
    Add-TextBox $slide 365 442 62 17 "更新需求" 7 $black $false 2 | Out-Null
    Add-TextBox $slide 466 436 40 21 "↻" 20 $purple $true 2 | Out-Null
    Add-TextBox $slide 537 442 62 17 "更新价格" 7 $black $false 2 | Out-Null
    Add-Arrow $slide 480 414 480 422 $purple 2.2 | Out-Null
    $da1 = Add-Arrow $slide 186 300 350 452 $orange 1.4 $true
    $da2 = Add-Arrow $slide 675 300 610 452 $orange 1.4 $true
    $da1.ZOrder(1)
    $da2.ZOrder(1)

    Add-TextBox $slide 690 123 240 19 "A. 主要结果" 13 $blue $true 1 | Out-Null
    Add-Metric $slide 690 150 116 48 "相对短视动态定价" "+5.22%" $green $green
    Add-Metric $slide 818 150 116 48 "相对统一定价" "+80.51%" $green $green
    Add-Metric $slide 690 208 116 48 "最低 QoS" "0.6632 → 0.9918" $blue $blue
    Add-Metric $slide 818 208 116 48 "账单保护下" "+21.29%" $red $red

    $gpuBox = Add-RoundBox $slide 683 270 259 106 (RgbColor 255 255 255) $purple 1.0
    Add-TextBox $slide 692 274 238 18 "B. 单 GPU 验证" 13 $blue $true 1 | Out-Null
    Add-LineChart $slide 700 298 222 70 $blue $red

    Add-TextBox $slide 690 386 240 18 "C. 稳健性检查" 13 $purple $true 1 | Out-Null
    $checks = @("容量变化", "账单保护", "市场扩张", "QoS 反馈")
    for ($i = 0; $i -lt 4; $i++) {
        $cx = 690 + 61 * $i
        $cb = Add-RoundBox $slide $cx 412 55 24 (RgbColor 255 255 255) $purple 0.9
        Set-Text $cb $checks[$i] 8 $black $true 2
    }

    Add-Arrow $slide 286 172 340 172 (RgbColor 56 142 60) 2.0 | Out-Null
    Add-TextBox $slide 292 136 48 30 "需求信息`n偏好/成本" 8 $black $false 2 | Out-Null
    Add-Arrow $slide 620 172 675 172 (RgbColor 56 142 60) 2.0 | Out-Null
    Add-TextBox $slide 628 136 48 30 "数据状态`n容量/QoS" 8 $black $false 2 | Out-Null

    $summary = Add-RoundBox $slide 12 506 936 26 $greenSoft $green 1.0
    Set-Text $summary "✓ QoS 感知的约束动态定价通过价格信号迁移弹性需求，在固定平均标价约束下缓解拥挤，并由仿真与单 GPU 测量共同支持。" 12 $black $true 2
    $legend = Add-RoundBox $slide 16 474 928 24 (RgbColor 255 255 255) (RgbColor 218 222 226) 0.6
    Set-Text $legend "绿色箭头：需求/状态信息流      蓝色箭头：价格信号流      橙色虚线：供给/反馈影响      紫色箭头：迭代更新" 9 $black $false 2

    if (Test-Path $pptxPath) { Remove-Item -LiteralPath $pptxPath -Force }
    if (Test-Path $previewPath) { Remove-Item -LiteralPath $previewPath -Force }
    $prs.SaveAs($pptxPath, 24)
    $slide.Export($previewPath, "PNG", 1600, 900)
    Write-Output "PPTX=$pptxPath"
    Write-Output "PREVIEW=$previewPath"
    Write-Output "SHAPES=$($slide.Shapes.Count)"
}
finally {
    if ($prs -ne $null) { $prs.Close() | Out-Null }
    if ($ppt -ne $null) { $ppt.Quit() | Out-Null }
    if ($slide -ne $null) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($slide) | Out-Null }
    if ($prs -ne $null) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($prs) | Out-Null }
    if ($ppt -ne $null) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
