Add-Type -AssemblyName System.Drawing
$ErrorActionPreference = 'Stop'
$dir = $PSScriptRoot
$n = 256
$bmp = [System.Drawing.Bitmap]::new($n, $n, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$p0 = [System.Drawing.Point]::new(0, 0)
$p1 = [System.Drawing.Point]::new($n, $n)
$c1 = [System.Drawing.Color]::FromArgb(37, 97, 199)
$c2 = [System.Drawing.Color]::FromArgb(15, 60, 140)
$lg = [System.Drawing.Drawing2D.LinearGradientBrush]::new($p0, $p1, $c1, $c2)
$rect = [System.Drawing.Rectangle]::new(0, 0, $n, $n)
$g.FillRectangle($lg, $rect)
$rr = 56
$x2 = $n - $rr; $y2 = $n - $rr
$gp = [System.Drawing.Drawing2D.GraphicsPath]::new()
$gp.AddArc(0, 0, $rr, $rr, 180, 90)
$gp.AddArc($x2, 0, $rr, $rr, 270, 90)
$gp.AddArc($x2, $y2, $rr, $rr, 0, 90)
$gp.AddArc(0, $y2, $rr, $rr, 90, 90)
$gp.CloseFigure()
$card = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(45, 255, 255, 255))
$g.FillPath($card, $gp)
$pen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(120, 255, 255, 255), [single]3)
$g.DrawPath($pen, $gp)
$f = [System.Drawing.Font]::new('Segoe UI', [single]150, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$sf = [System.Drawing.StringFormat]::new()
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center
$r = [System.Drawing.RectangleF]::new([single]0, [single](-8), [single]$n, [single]$n)
$g.DrawString('N', $f, [System.Drawing.Brushes]::White, $r, $sf)
$hIcon = $bmp.GetHicon()
$icon = [System.Drawing.Icon]::FromHandle($hIcon)
$fs = [System.IO.File]::Create((Join-Path $dir 'UnipusAI-Helper.ico'))
$icon.Save($fs)
$fs.Close()
$icon.Dispose()
$g.Dispose(); $bmp.Dispose()
Write-Output 'ICON_OK'
