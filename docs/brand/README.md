# Brand assets

These files identify the two sites linked from the FLASH README. The brand
marks retain their owners’ rights; the FLASH code’s MIT license does not grant
rights to these marks.

| File | Official source and use |
| --- | --- |
| `septlab-icon.png` | [SEPT Lab’s live 192px icon](https://septlab.com/assets/img/icon-192.png), downloaded without modification. It preserves the sun, tree, and seated figure used in the current site mark. |
| `verifiable-pro-icon.svg` | [verifiable.pro’s live favicon](https://verifiable.pro/assets/favicon.svg), copied without modification. Use this small-size cut below 24px. |
| `verifiable-pro-lockup.svg` | [verifiable.pro’s live light-background lockup](https://verifiable.pro/assets/logo-lockup.svg), copied without modification. The current brand guidance uses its master mark at 24px and above and the lockup at least 120px wide. |
| `presented-by-verifiable-pro.svg` | Reusable 112×20px editorial badge showing the official small-size mark and “verifiable.pro”. Its accessible title and hover text retain “Presented by verifiable.pro”. The mark is unchanged; only the surrounding credit layout is new. |
| `presented-by-verifiable-pro-lockup.svg` | Larger 218×52px editorial credit using the exact master-mark geometry and current wordmark styling. |

The current verifiable.pro identity is the graphite tile, monoline V, and red
square. The retired lime-green/checkmark identity in the site’s `brand/`
archive is not used. The SEPT icon is from the live site because the local
website checkout’s older favicon is a different simplified drawing.

“Presented by verifiable.pro” is an editorial presentation credit. ACM artifact
badges remain separate and link to the official ATC evaluation results.

Canonical destinations: [SEPT Lab](https://septlab.com/) and
[verifiable.pro](https://verifiable.pro/).

## Reuse the presentation badge

Place the compact badge beside paper, artifact, and license links:

```html
<a href="https://verifiable.pro/">
  <img src="docs/brand/presented-by-verifiable-pro.svg"
       alt="Presented by verifiable.pro" title="Presented by verifiable.pro" height="20">
</a>
```

For another repository, copy the badge with this provenance note and use a
local image path, or reference a stable raw-file URL after this change is
merged. Point the link at the corresponding verifiable.pro article when that
article is published; until then, use the site home page.
