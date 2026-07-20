# Concrete IoT Icon Candidates

This directory contains original icon files collected for author review. It
does not contain a composed framework figure, generated contact sheet, or
ImageGen output.

## Sources

### Microsoft Fluent Emoji

- Repository: <https://github.com/microsoft/fluentui-emoji>
- Pinned commit: `62ecdc0d7ca5c6df32148c169556bc8d3782fca4`
- Licence: MIT
- Selection: 36 concepts, each saved as the original 256x256 transparent 3D
  PNG and the corresponding colour SVG.
- Intended role: devices, workload timing, cloud/network symbols, status
  indicators, market actors, and financial objects.

### 3dicons

- Repository: <https://github.com/realvjy/3dicons>
- Pinned commit: `8884d59e68a7bae0e0e2163af5b6c2ad992c01c8`
- Licence: CC0 1.0 Universal
- Selection: 20 original 400x400 transparent dynamic-colour PNG files from
  the asset URLs recorded in the upstream metadata.
- Intended role: a more dimensional alternative for computers, mobile
  devices, chat, time, networking, settings, metrics, security, and money.

### Streamline Ultimate Color

- Repository: <https://github.com/webalys-hq/streamline-vectors>
- Pinned commit: `52d750c9ce051e51cb181b7a78932120c48541d0`
- Licence: CC BY 4.0; attribution to Streamline is required.
- Selection: 48 original SVG files from the `ultimate/colors` family.
- Intended role: the preferred source for the supplied reference style:
  dark outlines, light neutral bodies, and restrained multicolour fills.
- Technical coverage: IoT endpoints, users, providers, API routing, servers,
  compute chips, QoS, dynamic pricing, time slots, and simulation evidence.

The two sources are kept in separate folders. Their styles should be compared
before manuscript use and should not be mixed casually in one figure.

## Directory layout

```text
iot_icon_candidates/
├── SOURCES.tsv
├── streamline_ultimate_color/
│   ├── svg/
│   ├── SOURCES.tsv
│   ├── ATTRIBUTION.md
│   ├── LICENSE-CC-BY-4.0.txt
│   └── README.md
├── fluentui_emoji/
│   ├── 3d_png/
│   ├── color_svg/
│   └── LICENSE-MIT.txt
└── 3dicons/
    ├── color_png/
    └── LICENSE-CC0.txt
```

`SOURCES.tsv` records the source repository, semantic category, upstream name,
local slug, and exact source path or URL for every copied asset.

The Streamline selection keeps its own detailed `SOURCES.tsv` because it maps
paper roles to the upstream repository tree. It should be preferred for a
framework figure matching the latest visual reference.

## Manuscript boundary

These files are candidates only. No icon has been inserted into Figure 1 or
the TeX manuscript. The IconPark server/GPU assets remain available separately
for technical concepts not represented by either 3D collection.
