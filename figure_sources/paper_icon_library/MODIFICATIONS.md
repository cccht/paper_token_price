# IconPark derivative modifications

The files under `upstream_svg/` are copied without modification from the
ByteDance IconPark repository at commit
`8dc132da4c85671ba6a5962c87aa2bdafbf158e9`.

The generated Draw.io library and contact sheets are derivative renderings.
The build script makes only the following visual substitutions:

- black strokes and fills are replaced with the semantic category colour;
- IconPark blue fills (`#2F88FF`) are replaced with the same category colour;
- IconPark cyan fills (`#43CCF8`) are replaced with a lighter category colour;
- white fills and strokes are retained;
- a modification comment containing the upstream commit is inserted into each
  generated SVG payload.

No path geometry, view box, icon name, or source SVG is changed. The generated
contact sheet adds labels, grouping panels, and `core`/`optional` badges that
are original to this manuscript project.

The source and derivative files are distributed under the included
Apache License 2.0. The original project is available at
<https://github.com/bytedance/IconPark>.

