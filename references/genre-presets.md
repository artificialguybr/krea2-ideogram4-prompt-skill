# Presets por gênero (templates EN prontos)

Preencha os `<...>`. Remova módulos irrelevantes. Sempre entregue no Output Profile (SKILL.md).

## 1. Fotografia / retrato editorial
```
Editorial 85mm portrait of <subject>, <appearance with textures>, <pose>. Shot on <camera/film> at f/1.8, shallow depth of field, <framing>. <environment with 2–3 depth layers>. <source+direction+quality of light>. <color story via materials>. <mood via mechanism, not adjectives>.
Settings: Krea 2 Large (hosted) ou RAW; aspect 4:5; sliders: intensity −20, complexity 0, movement −10; creativity baixa-média.
```

## 2. Fashion / try-on
```
<Model description> wearing <garment with fabric, weight, drape>, <pose>. <studio or location>. <light>. <color palette via materials>. Sharp fabric texture, natural skin.
Settings: Krea 2 Large; pós: Identity Edit p/ trocar roupa (editing.md §3).
```

## 3. Pôster / print gráfico (Ideogram 4 JSON recomendado)
- Ir de JSON: `art_style` (NUNCA `photo`), textos como elementos próprios com bbox, paleta em hex ≤16.
```
high_level_description: "<tema do poster>"
style_description.art_style: { movement: <>, medium: "screenprint poster", surface: <>, line_quality: <> }
elements: [ { text: "HEADLINE ≤4 PALAVRAS", bbox: [...] }, { object: "<visual>", bbox: [...], color_palette: [...] } ]
Settings: V4_QUALITY_48; aspect 2:3; conferir OCR em 100%.
```

## 4. UI / web / app mockup
```
Clean <device> mockup floating over <background>, screen showing <UI description>. Soft studio light from upper left, gentle shadow. Minimal composition, generous negative space. <accent color via hex/material>.
Settings: Ideogram 4 JSON (controle) ou Krea Medium; aspect 16:10 / 4:3.
```

## 5. 3D / render
```
<subject> as a <matte/glossy/clay> 3D render, <form details>, floating over <studio backdrop>. Soft key light upper left + rim light from behind. Subtle subsurface scattering / bevel highlights. Octane-style path tracing, clean topology read.
Settings: Krea 2 Medium; sliders: complexity −30 (forma limpa), movement 0; creativity média-alta.
```

## 6. Anime / ilustração
```
<subject> in <anime/illustration style + era/studio reference>, <outfit>, <expression>, <action>. Background: <environment, painterly depth>. Cel shading with soft gradient shadows, clean lineart, <color script>. Composition: <angle/framing>.
Settings: Krea 2 Medium; aspect conforme composição.
```

## 7. Produto / e-commerce
```
<Product> in <material/finish>, <hero angle>, on <surface/prop>. <light: source+direction+quality>. Background <clean positive constraint>. Crisp edges, true-to-life color, subtle reflection.
Settings: Krea 2 Large/RAW; creativity baixa.
```

## 8. Cena cinematográfica
```
<establishing shot description>. <camera movement feel: dolly-in/wide static/handheld>. <time of day + light source>. <weather/atmosphere via mechanism>. <color grade via palette/materials>. Anamorphic feel, gentle lens flare.
Settings: RAW 52 steps / V4_QUALITY_48; aspect 21:9 ou 16:9.
```

## 9. Arquitetura / interior
```
<space> with <materials: concrete/oak/linen...>, <furniture>. <natural/artificial light source + direction>. <human scale element>. Photoreal, verticals true, <lens> perspective.
Settings: Krea 2 Large; aspect 4:5 / 3:2.
```

## 10. Variações de família consistente (batch)
- Trave: seed-like contract = mesmo JSON (Ideogram) ou mesmo bloco [Subject hierarchy]+[Appearance]; varie 1 dimensão (expressão/ângulo/estação). Documente a variável no campo ASSUMPTIONS.

## 11. Notas transversais (v2)

- Sliders Krea (intensity/complexity/movement, −100..100) vão em SUGGESTED SETTINGS para todo preset hosted.
- Para texto denso (signage, menu, packaging) prefira **Ideogram 4.0/4.5** (também dentro do app Krea) ou Seedream — Krea 2 é o ponto fraco de texto longo.
- Pôster/print em Ideogram: gerar JSON (§3 do preset) com Expand Prompt OFF na 2ª rodada para travar o copy.
- Variações de família consistente: no 4.5 use seed + mesmo tier; no 4.0 use o JSON loop.
