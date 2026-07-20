# Icon sources for the inference-pricing Draw.io framework

Prepared: 2026-07-10

## Selected library

The diagram uses SVG icons from **Font Awesome Free 7.3.0**, downloaded from
the official [Font Awesome repository](https://github.com/FortAwesome/Font-Awesome/tree/7.3.0).
Font Awesome Free SVG icons are distributed under the
[Creative Commons Attribution 4.0 licence](https://fontawesome.com/license/free).
The downloaded SVG files retain the upstream attribution comment.

The following source SVG icons are recoloured by the build script, rendered to
512-pixel transparent PNG assets, and embedded directly in the Draw.io source:

- `users.svg`
- `clock.svg`
- `calendar-days.svg`
- `cloud.svg`
- `server.svg`
- `door-open.svg`
- `gauge-high.svg`
- `shield-halved.svg`
- `tags.svg`
- `route.svg`
- `microchip.svg`
- `bullseye.svg`
- `chart-column.svg`

Local source directory:

```text
figure_sources/fontawesome-free-7.3.0/
```

## Selection rationale

The icons are generic computing and interface symbols rather than copied
scientific artwork. A single family was used to keep stroke, silhouette, and
visual weight consistent across the user, intermediary, provider, serving, and
diagnostic layers. BioIcons and other open scientific-illustration collections
were reviewed, but their biology-oriented assets were not mixed into this
computing-market diagram.

## Reuse note

The Draw.io layout, labels, arrows, and colour treatment are original to this
manuscript. Font Awesome attribution and licence information must remain with
the editable source package when the figure is redistributed. The original SVG
files are retained locally so the icons can be recoloured and regenerated
without downloading external assets. The SVG-to-PNG embedding step is used
because the tested Draw.io 30.3.6 command-line exporter did not render embedded
SVG Data URIs reliably; labels, connectors, borders, and panel geometry remain
vector objects in the SVG and PDF exports.
