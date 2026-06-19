param(
    [string]$OutputDir = $PSScriptRoot,
    [string]$BaseName = "three_layer_game_framework_visio"
)

$ErrorActionPreference = "Stop"
$PageW = 16.0
$PageH = 9.8

$Colors = @{
    Ink = "RGB(23,32,42)"
    Muted = "RGB(95,111,130)"
    Line = "RGB(215,224,234)"
    Green = "RGB(37,139,71)"
    Blue = "RGB(11,115,199)"
    Navy = "RGB(18,59,99)"
    Orange = "RGB(243,154,18)"
    Purple = "RGB(112,66,165)"
    Violet = "RGB(77,35,120)"
    Cloud = "RGB(234,246,255)"
    Card = "RGB(255,255,255)"
    Tile = "RGB(248,252,255)"
}

function Y([double]$y) { return $script:PageH - $y }

function Set-Cell($Shape, [string]$Cell, [string]$Formula) {
    try { $Shape.CellsU($Cell).FormulaU = $Formula } catch {}
}

function Style-Line($Shape, [string]$Color, [double]$Weight = 1.2, [bool]$Dashed = $false) {
    Set-Cell $Shape "LineColor" $Color
    Set-Cell $Shape "LineWeight" "$Weight pt"
    if ($Dashed) { Set-Cell $Shape "LinePattern" "2" }
}

function Style-Fill($Shape, [string]$Fill, [string]$Line, [double]$Weight = 1.2, [bool]$Dashed = $false) {
    Set-Cell $Shape "FillForegnd" $Fill
    Set-Cell $Shape "FillPattern" "1"
    Style-Line $Shape $Line $Weight $Dashed
}

function Style-Text($Shape, [double]$Size, [string]$Color, [bool]$Bold = $false, [int]$Align = 1) {
    Set-Cell $Shape "Char.Font" "FONT(""Calibri"")"
    Set-Cell $Shape "Char.Size" "$Size pt"
    Set-Cell $Shape "Char.Color" $Color
    Set-Cell $Shape "Para.HorzAlign" "$Align"
    Set-Cell $Shape "VerticalAlign" "1"
    Set-Cell $Shape "LeftMargin" "0.04 in"
    Set-Cell $Shape "RightMargin" "0.04 in"
    if ($Bold) { Set-Cell $Shape "Char.Style" "1" } else { Set-Cell $Shape "Char.Style" "0" }
}

function Add-Rect([double]$x, [double]$y, [double]$w, [double]$h, [string]$Fill, [string]$Line,
                  [double]$Weight = 1.2, [double]$Round = 0.08, [bool]$Dashed = $false) {
    $s = $script:Page.DrawRectangle($x, (Y ($y + $h)), ($x + $w), (Y $y))
    Style-Fill $s $Fill $Line $Weight $Dashed
    Set-Cell $s "Rounding" "$Round in"
    return $s
}

function Add-Text([double]$x, [double]$y, [double]$w, [double]$h, [string]$Body,
                  [double]$Size, [string]$Color, [bool]$Bold = $false, [int]$Align = 1) {
    $s = $script:Page.DrawRectangle($x, (Y ($y + $h)), ($x + $w), (Y $y))
    Set-Cell $s "FillPattern" "0"
    Set-Cell $s "LinePattern" "0"
    $s.Text = $Body
    Style-Text $s $Size $Color $Bold $Align
    return $s
}

function Add-Line([double]$x1, [double]$y1, [double]$x2, [double]$y2, [string]$Color,
                  [double]$Weight = 2.0, [bool]$Arrow = $true, [bool]$Dashed = $false) {
    $s = $script:Page.DrawLine($x1, (Y $y1), $x2, (Y $y2))
    Style-Line $s $Color $Weight $Dashed
    if ($Arrow) { Set-Cell $s "EndArrow" "13" }
    return $s
}

function Add-IconBox([double]$x, [double]$y, [string]$Label, [string]$Color) {
    $box = Add-Rect $x $y 0.55 0.48 "RGB(249,252,255)" $Color 1.4 0.09
    $box.Text = $Label
    Style-Text $box 15 $Color $true 1
}

function Add-AppCard([double]$y, [string]$Title, [string]$Body, [string]$Symbol, [string]$Color) {
    Add-Rect 0.48 $y 3.45 0.96 $Colors.Card $Colors.Line 1.1 0.18 | Out-Null
    Add-IconBox 0.76 ($y + 0.27) $Symbol $Color
    Add-Text 1.58 ($y + 0.19) 1.95 0.28 $Title 16 $Color $true 0 | Out-Null
    Add-Text 1.58 ($y + 0.51) 2.00 0.32 $Body 10.5 $Colors.Muted $false 0 | Out-Null
}

function Add-Label([double]$x, [double]$y, [string]$Title, [string]$Sub, [string]$Color) {
    Add-Rect ($x - 0.88) ($y - 0.23) 1.76 0.48 "RGB(255,255,255)" "RGB(225,232,240)" 0.9 0.08 | Out-Null
    Add-Text ($x - 0.78) ($y - 0.17) 1.56 0.18 $Title 11.2 $Color $true 1 | Out-Null
    Add-Text ($x - 0.78) ($y + 0.03) 1.56 0.16 $Sub 8.4 $Colors.Muted $true 1 | Out-Null
}

function Add-Tile([double]$x, [string]$Title, [string]$Body) {
    $s = Add-Rect $x 4.56 1.06 0.66 $Colors.Card "RGB(93,166,232)" 1.2 0.10
    $s.Text = "$Title`n$Body"
    Style-Text $s 10.8 $Colors.Blue $true 1
}

function Add-Chip([double]$x, [double]$y, [string]$Name, [string]$Dot) {
    Add-Rect $x $y 1.28 0.34 "RGB(251,250,255)" "RGB(217,201,239)" 0.9 0.08 | Out-Null
    $dotShape = $script:Page.DrawOval(($x + 0.12), (Y ($y + 0.24)), ($x + 0.25), (Y ($y + 0.11)))
    Style-Fill $dotShape $Dot $Dot 0.1
    Add-Text ($x + 0.32) ($y + 0.07) 0.88 0.19 $Name 9.0 $Colors.Ink $true 0 | Out-Null
}

function Add-Cloud() {
    $cloudShapes = @()
    $cloudShapes += $script:Page.DrawOval(4.90, (Y 3.77), 7.05, (Y 1.88))
    $cloudShapes += $script:Page.DrawOval(6.20, (Y 3.45), 8.70, (Y 1.33))
    $cloudShapes += $script:Page.DrawOval(7.85, (Y 3.83), 10.05, (Y 1.93))
    $cloudShapes += Add-Rect 4.72 2.65 5.52 1.52 $Colors.Cloud "RGB(93,166,232)" 2.6 0.42
    foreach ($s in $cloudShapes) { Style-Fill $s $Colors.Cloud "RGB(93,166,232)" 2.6 }
    Add-Text 6.95 2.10 1.80 0.46 "OpenRouter-like`nAPI Intermediary" 14 $Colors.Navy $true 1 | Out-Null
    Add-Rect 6.00 2.78 0.58 1.00 "RGB(24,61,99)" "RGB(13,43,71)" 1.0 0.05 | Out-Null
    Add-Rect 6.73 2.52 0.70 1.26 "RGB(24,61,99)" "RGB(13,43,71)" 1.0 0.05 | Out-Null
    $g1 = $script:Page.DrawOval(6.23, (Y 3.25), 6.34, (Y 3.14)); Style-Fill $g1 "RGB(85,213,138)" "RGB(85,213,138)" 0.1
    $g2 = $script:Page.DrawOval(7.02, (Y 3.00), 7.13, (Y 2.89)); Style-Fill $g2 "RGB(85,213,138)" "RGB(85,213,138)" 0.1
    $api = Add-Rect 7.93 2.94 1.42 0.62 "RGB(255,255,255)" "RGB(124,184,230)" 1.7 0.06
    $api.Text = "API"
    Style-Text $api 18 $Colors.Blue $true 1
}

function Add-Suppliers() {
    Add-Rect 12.00 1.78 3.58 4.52 $Colors.Card $Colors.Line 1.1 0.20 | Out-Null
    Add-Text 12.58 2.02 2.48 0.30 "Model API Providers" 15 $Colors.Violet $true 1 | Out-Null
    Add-Chip 12.24 2.62 "DeepSeek" "RGB(43,118,210)"
    Add-Chip 13.72 2.62 "Claude" "RGB(192,107,62)"
    Add-Chip 12.24 3.08 "GPT / OpenAI" "RGB(24,166,122)"
    Add-Chip 13.72 3.08 "Gemini/Qwen" "RGB(142,91,211)"
    Add-Line 12.24 4.08 15.34 4.08 "RGB(228,233,240)" 1.0 $false | Out-Null
    $gpu = Add-Rect 12.24 4.25 3.10 0.78 "RGB(249,251,254)" "RGB(223,231,239)" 0.9 0.12
    $gpu.Text = "GPU      GPU pools, cloud regions`n         API quota and SLA capacity"
    Style-Text $gpu 10.4 $Colors.Muted $false 0
    Add-Line 12.24 5.23 15.34 5.23 "RGB(228,233,240)" 1.0 $false | Out-Null
    $cost = Add-Rect 12.24 5.40 3.10 0.78 "RGB(249,251,254)" "RGB(223,231,239)" 0.9 0.12
    $cost.Text = "c         marginal cost, latency`n          availability and incident state"
    Style-Text $cost 9.8 $Colors.Muted $false 0
}

function Add-Game() {
    Add-Rect 4.55 6.15 6.80 1.28 "RGB(255,255,255)" $Colors.Blue 1.3 0.16 $true | Out-Null
    Add-Text 5.58 6.32 4.78 0.28 "Dynamic Pricing & Stackelberg Game" 15.5 $Colors.Navy $true 1 | Out-Null
    $steps = @(
        @(4.82, "D_jt", "Demand"),
        @(6.48, "p_jt", "Retail price"),
        @(8.14, "g_jt", "Capacity route"),
        @(9.80, "profit, q", "Profit / QoS")
    )
    foreach ($st in $steps) {
        $s = Add-Rect $st[0] 6.82 1.05 0.48 "RGB(249,252,255)" "RGB(184,217,243)" 0.9 0.10
        $s.Text = "$($st[1])`n$($st[2])"
        Style-Text $s 9.2 $Colors.Blue $true 1
    }
    Add-Line 5.88 7.06 6.44 7.06 "RGB(139,148,158)" 1.6 | Out-Null
    Add-Line 7.54 7.06 8.10 7.06 "RGB(139,148,158)" 1.6 | Out-Null
    Add-Line 9.20 7.06 9.76 7.06 "RGB(139,148,158)" 1.6 | Out-Null
}

function Add-Feedback() {
    Add-Rect 5.25 8.05 5.62 0.76 "RGB(255,254,255)" "RGB(184,151,222)" 1.3 0.16 $true | Out-Null
    Add-Text 5.88 8.18 4.36 0.20 "Iterative Feedback (Game Equilibrium)" 13.5 $Colors.Purple $true 1 | Out-Null
    Add-Text 5.94 8.54 1.45 0.18 "update demand" 9.2 $Colors.Muted $true 1 | Out-Null
    $mid = Add-Rect 7.55 8.42 0.95 0.28 "RGB(247,241,255)" "RGB(200,168,232)" 0.8 0.10
    $mid.Text = "SUE / SPE"
    Style-Text $mid 11.5 $Colors.Purple $true 1
    Add-Text 8.78 8.54 1.68 0.18 "update price & routing" 9.2 $Colors.Muted $true 1 | Out-Null
}

function Add-Legend() {
    Add-Rect 0.40 9.12 15.20 0.38 "RGB(255,255,255)" $Colors.Line 0.9 0.10 | Out-Null
    $items = @(
        @(0.90, $Colors.Green, "Information Flow"),
        @(3.95, $Colors.Blue, "Price / Signal Flow"),
        @(7.35, $Colors.Orange, "Token / Capacity Flow"),
        @(10.85, $Colors.Purple, "Feedback / Iteration")
    )
    foreach ($i in $items) {
        Add-Line $i[0] 9.31 ($i[0] + 0.55) 9.31 $i[1] 2.0 | Out-Null
        Add-Text ($i[0] + 0.75) 9.20 1.62 0.20 $i[2] 9.0 $Colors.Ink $false 0 | Out-Null
    }
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$vsdx = Join-Path $OutputDir "$BaseName.vsdx"
$pdf = Join-Path $OutputDir "$BaseName.pdf"

$visio = New-Object -ComObject Visio.Application
$visio.Visible = $false
$visio.AlertResponse = 7
$doc = $visio.Documents.Add("")
$script:Page = $visio.ActivePage
$script:Page.PageSheet.CellsU("PageWidth").ResultIU = $PageW
$script:Page.PageSheet.CellsU("PageHeight").ResultIU = $PageH
$script:Page.Name = "Three-layer game framework"

Add-Text 1.65 0.25 1.15 0.32 "Users" 18 $Colors.Green $true 1 | Out-Null
Add-Text 1.32 0.60 1.82 0.24 "(Applications / API Loads)" 11.2 $Colors.Green $true 1 | Out-Null
Add-Text 5.28 0.25 5.44 0.32 "Cloud Platform / API Intermediary" 18 $Colors.Navy $true 1 | Out-Null
Add-Text 6.32 0.60 3.36 0.24 "(OpenRouter-like Aggregator)" 11.2 $Colors.Navy $true 1 | Out-Null
Add-Text 11.42 0.25 4.42 0.32 "Model Manufacturers / Suppliers" 17 $Colors.Violet $true 1 | Out-Null
Add-Text 12.52 0.60 2.74 0.24 "(LLM APIs & Compute Grid)" 10.8 $Colors.Violet $true 1 | Out-Null

Add-AppCard 1.72 "Chat Apps" "consumer queries`nelastic timing" "..." $Colors.Green
Add-AppCard 2.98 "Coding Agents" "batch jobs`nretry and fallback" ">_" "RGB(65,105,168)"
Add-AppCard 4.24 "Enterprise APIs" "workflow calls`nSLA-sensitive demand" "N" "RGB(35,134,111)"
Add-AppCard 5.50 "Developers / SDK" "client calls`nmodel-time choice" "{/}" "RGB(46,139,87)"
Add-Cloud
Add-Tile 5.05 "DB" "usage data"
Add-Tile 6.60 "FC" "forecast"
Add-Tile 8.15 "OPT" "pricing"
Add-Tile 9.70 "QoS" "monitor"
Add-Suppliers
Add-Game
Add-Feedback

Add-Line 3.94 2.98 5.07 2.98 $Colors.Green 2.0 | Out-Null
Add-Label 4.70 2.65 "Information" "demand, preference" $Colors.Green
Add-Line 5.07 3.88 3.94 3.88 $Colors.Blue 2.0 | Out-Null
Add-Label 4.70 4.22 "Price / Signals" "retail, incentives" $Colors.Blue
Add-Line 12.13 2.98 10.88 2.98 $Colors.Green 2.0 | Out-Null
Add-Label 11.40 2.65 "Data / Status" "capacity, cost" $Colors.Green
Add-Line 10.88 3.88 12.13 3.88 $Colors.Blue 2.0 | Out-Null
Add-Label 11.40 4.22 "Price / Contracts" "wholesale, quota" $Colors.Blue
Add-Line 8.00 5.22 8.00 6.15 "RGB(139,148,158)" 1.7 | Out-Null
Add-Line 3.93 6.00 5.23 8.42 $Colors.Orange 2.0 $true $true | Out-Null
Add-Label 3.92 7.72 "Response" "load shifting" $Colors.Orange
Add-Line 12.14 6.00 10.88 8.42 $Colors.Orange 2.0 $true $true | Out-Null
Add-Label 12.10 7.72 "Token Supply" "quota, capacity" $Colors.Orange
Add-Line 8.00 7.43 8.00 8.05 $Colors.Purple 2.0 | Out-Null
Add-Legend

$doc.SaveAs($vsdx)
$doc.ExportAsFixedFormat(1, $pdf, 1, 0)
$doc.Close()
$visio.Quit()

Write-Output "Generated:"
Write-Output $vsdx
Write-Output $pdf
