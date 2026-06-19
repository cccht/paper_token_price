param(
    [string]$OutputDir = $PSScriptRoot,
    [string]$BaseName = "api_market_topology_visio"
)

$ErrorActionPreference = "Stop"
$PageW = 13.5; $PageH = 7.2
$Black  = "RGB(0,0,0)"; $DGray = "RGB(70,70,70)"; $LGray = "RGB(160,160,160)"
$White  = "RGB(255,255,255)";  $Bg    = "RGB(248,248,248)"

function Y([double]$y) { return $script:PageH - $y }

function Set-Cell($s,[string]$c,[string]$v) { try{$s.CellsU($c).FormulaU=$v}catch{} }

function Rect($x,$y,$w,$h,$fill,$line,$lw=1.2,$round=0.08,$dash=$false) {
    $s=$script:Page.DrawRectangle($x,(Y($y+$h)),($x+$w),(Y $y))
    Set-Cell $s "FillForegnd" $fill; Set-Cell $s "FillPattern" "1"
    Set-Cell $s "LineColor" $line; Set-Cell $s "LineWeight" "$lw pt"
    Set-Cell $s "Rounding" "$round in"
    if($dash){Set-Cell $s "LinePattern" "2"}
    return $s
}

function Text($x,$y,$w,$h,$body,$size,$color,$bold=$false,$align=1) {
    $s=$script:Page.DrawRectangle($x,(Y($y+$h)),($x+$w),(Y $y))
    Set-Cell $s "FillPattern" "0"; Set-Cell $s "LinePattern" "0"
    $s.Text=$body
    Set-Cell $s "Char.Font" "FONT(""Calibri"")"; Set-Cell $s "Char.Size" "$size pt"
    Set-Cell $s "Char.Color" $color; Set-Cell $s "Para.HorzAlign" "$align"; Set-Cell $s "VerticalAlign" "1"
    Set-Cell $s "LeftMargin" "0.06 in"; Set-Cell $s "RightMargin" "0.06 in"
    if($bold){Set-Cell $s "Char.Style" "1"}else{Set-Cell $s "Char.Style" "0"}
    return $s
}

function Arrow($x1,$y1,$x2,$y2,$dash=$false,$lw=1.3) {
    $s=$script:Page.DrawLine($x1,(Y$y1),$x2,(Y$y2))
    Set-Cell $s "LineColor" $DGray; Set-Cell $s "LineWeight" "$lw pt"
    Set-Cell $s "EndArrow" "13"
    if($dash){Set-Cell $s "LinePattern" "2"}
    return $s
}

function Block($x,$y,$w,$h,$title,$sub,$dash=$false) {
    Rect $x $y $w $h $Bg $Black 1.2 0.08 $dash | Out-Null
    Text ($x+0.12) ($y+0.10) ($w-0.24) 0.28 $title 12 $Black $true 0 | Out-Null
    Text ($x+0.12) ($y+0.42) ($w-0.24) ($h-0.56) $sub 9.5 $DGray $false 0 | Out-Null
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$vsdx=Join-Path $OutputDir "$BaseName.vsdx"
$pdf=Join-Path $OutputDir "$BaseName.pdf"

$visio=New-Object -ComObject Visio.Application; $visio.Visible=$false; $visio.AlertResponse=7
$doc=$visio.Documents.Add("")
$script:Page=$visio.ActivePage
$script:Page.PageSheet.CellsU("PageWidth").ResultIU=$PageW
$script:Page.PageSheet.CellsU("PageHeight").ResultIU=$PageH
$script:Page.Name="API Market Topology"

# ── Top: Exogenous Supply ─────────────────────
Block 2.50 0.50 8.50 1.50 "Exogenous Model API Supply" "DeepSeek / Claude / GPT / Gemini, Qwen and other API inputs`nGPU pools, API quota, SLA capacity, marginal cost input" $true

# ── Middle: Platform ──────────────────────────
Block 4.00 2.50 5.50 1.30 "Platform Wholesale Layer" "Sets wholesale price w_t; observes settlement and QoS" $false

# ── Middle-Lower: Broker & Direct ─────────────
Block 0.80 4.30 5.20 2.00 "Brokered Retail APIs" "Broker 1: p_1t, g_1t   Broker 2: p_2t, g_2t`nBroker 3: p_3t, g_3t`nOpenRouter-like aggregator model" $false
Block 7.50 4.30 5.20 2.00 "Direct API Channel (j = 0)" "Outside option: pD_t, gD_t`nPlatform self-operated`nSLA-guaranteed reserve capacity" $false

# ── Users ─────────────────────────────────────
Block 4.00 6.80 5.50 0.55 "User Classes & Time Slots" "Choose broker / direct channel / shift across periods" $false

# ── Arrows ────────────────────────────────────
Arrow 6.75 2.00 6.75 2.50         # supply→platform
Arrow 5.20 3.80 3.40 4.30         # platform→broker
Arrow 8.30 3.80 10.10 4.30        # platform→direct
Arrow 3.40 6.30 5.20 6.80         # broker→users
Arrow 10.10 6.30 8.30 6.80        # direct→users

# ── Annotations ──────────────────────────────
Text 1.00 5.80 2.20 0.24 "Brokered path" 9 $DGray $true 1
Text 10.50 5.80 2.20 0.24 "Outside option" 9 $DGray $true 1

# ── Separator ────────────────────────────────
Rect 0.40 2.25 12.7 0.01 $White $LGray 0.5 0 | Out-Null
Rect 0.40 4.05 12.7 0.01 $White $LGray 0.5 0 | Out-Null

$doc.SaveAs($vsdx)
$doc.ExportAsFixedFormat(1,$pdf,1,0)
$doc.Close(); $visio.Quit()
Write-Output "Generated: $vsdx`n$pdf"
