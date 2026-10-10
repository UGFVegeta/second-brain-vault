// Mini-Rasterizer fuer ldr_render.py: Z-Buffer, flache Farben, Linien mit Tiefentest.
// Eingabe: int32 W,H,NT,NL; NT * (float v[9], uint8 c[4]); NL * (float v[6], uint8 c[4])
// Ausgabe: W*H*4 Bytes (RGB + Alpha 255 wenn belegt)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

typedef struct { float v[9]; uint8_t c[4]; } Tri;
typedef struct { float v[6]; uint8_t c[4]; } Lin;

static inline float fminf3(float a, float b, float c) { return fminf(a, fminf(b, c)); }
static inline float fmaxf3(float a, float b, float c) { return fmaxf(a, fmaxf(b, c)); }

int main(int argc, char **argv) {
    if (argc < 3) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 2;
    int32_t hdr[4];
    if (fread(hdr, 4, 4, f) != 4) return 3;
    int W = hdr[0], H = hdr[1], NT = hdr[2], NL = hdr[3];
    Tri *T = malloc(sizeof(Tri) * (NT > 0 ? NT : 1));
    Lin *L = malloc(sizeof(Lin) * (NL > 0 ? NL : 1));
    if (NT && fread(T, sizeof(Tri), NT, f) != (size_t)NT) return 4;
    if (NL && fread(L, sizeof(Lin), NL, f) != (size_t)NL) return 5;
    fclose(f);
    float *zb = malloc(sizeof(float) * W * H);
    uint8_t *img = calloc((size_t)W * H * 4, 1);
    for (long i = 0; i < (long)W * H; i++) zb[i] = 1e30f;

    for (int t = 0; t < NT; t++) {
        float *v = T[t].v;
        float x0 = v[0], y0 = v[1], z0 = v[2], x1 = v[3], y1 = v[4], z1 = v[5], x2 = v[6], y2 = v[7], z2 = v[8];
        float minx = fminf3(x0, x1, x2), maxx = fmaxf3(x0, x1, x2), miny = fminf3(y0, y1, y2), maxy = fmaxf3(y0, y1, y2);
        int ix0 = (int)floorf(minx), ix1 = (int)ceilf(maxx), iy0 = (int)floorf(miny), iy1 = (int)ceilf(maxy);
        if (ix1 < 0 || iy1 < 0 || ix0 >= W || iy0 >= H) continue;
        if (ix0 < 0) ix0 = 0; if (iy0 < 0) iy0 = 0; if (ix1 >= W) ix1 = W - 1; if (iy1 >= H) iy1 = H - 1;
        float den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2);
        if (fabsf(den) < 1e-9f) continue;
        float inv = 1.0f / den;
        for (int y = iy0; y <= iy1; y++) {
            float py = y + 0.5f;
            for (int x = ix0; x <= ix1; x++) {
                float px = x + 0.5f;
                float a = ((y1 - y2) * (px - x2) + (x2 - x1) * (py - y2)) * inv;
                float b = ((y2 - y0) * (px - x2) + (x0 - x2) * (py - y2)) * inv;
                float c = 1.0f - a - b;
                if (a < -1e-4f || b < -1e-4f || c < -1e-4f) continue;
                float z = a * z0 + b * z1 + c * z2;
                long idx = (long)y * W + x;
                if (z < zb[idx]) {
                    zb[idx] = z;
                    uint8_t *p = img + idx * 4;
                    p[0] = T[t].c[0]; p[1] = T[t].c[1]; p[2] = T[t].c[2]; p[3] = 255;
                }
            }
        }
    }
    // Linien (Kanten) mit Tiefenbias
    for (int l = 0; l < NL; l++) {
        float *v = L[l].v;
        float dx = v[3] - v[0], dy = v[4] - v[1];
        int n = (int)(fmaxf(fabsf(dx), fabsf(dy))) + 1;
        if (n > 4000) continue;
        for (int i = 0; i <= n; i++) {
            float s = (float)i / n;
            int x = (int)floorf(v[0] + dx * s), y = (int)floorf(v[1] + dy * s);
            if (x < 0 || y < 0 || x >= W || y >= H) continue;
            float z = v[2] + (v[5] - v[2]) * s;
            long idx = (long)y * W + x;
            if (z <= zb[idx] + 1.2f) {
                uint8_t *p = img + idx * 4;
                p[0] = L[l].c[0]; p[1] = L[l].c[1]; p[2] = L[l].c[2]; p[3] = 255;
            }
        }
    }
    FILE *o = fopen(argv[2], "wb");
    fwrite(img, 1, (size_t)W * H * 4, o);
    fclose(o);
    return 0;
}
