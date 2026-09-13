# Juan Cafe Till — Android app

Ang POS na ginawa natin, naka-package bilang tunay na Android app. Ang buong
till ay nasa loob mismo ng APK, kaya **gumagana kahit walang internet** — nasa
tablet mismo ang lahat ng benta, stock at shift records.

Dalawang bagay ang naidagdag ng app na hindi kaya ng browser:

- **Bluetooth thermal printer (ESC/POS)** — awtomatikong pag-print ng resibo
  pagkatapos ng bawat bayad, at ng end-of-day report pagsara.
- **Cash drawer kick** — bubukas ang drawer kapag cash ang bayad, kung
  nakasaksak ito sa RJ11 port ng printer.

---

## 1. Ano ang kailangan

- **Android Studio** (libre, Windows o Mac) — [developer.android.com/studio](https://developer.android.com/studio)
- Android tablet o phone, **Android 7.0 (API 24) pataas**
- Thermal printer na **classic Bluetooth (SPP)** — karaniwang 58mm o 80mm POS printer

Kung ayaw nyong mag-install ng Android Studio, tingnan ang **Seksyon 6** —
puwedeng ang GitHub na ang mag-build ng APK para sa inyo.

---

## 2. Pag-build ng APK

1. Buksan ang Android Studio → **Open** → piliin ang folder na `JuanCafeTill`.
2. Hintayin ang unang Gradle sync. Dito i-download nito ang Gradle at ang
   Android build tools — mga 5–15 minuto depende sa internet. **Kailangan ng
   internet sa unang build lang**; pagkatapos, offline na puwede.
3. Kapag tapos na ang sync: **Build → Build Bundle(s) / APK(s) → Build APK(s)**.
4. Lalabas ang APK dito:

   ```
   app/build/outputs/apk/debug/app-debug.apk
   ```

Sa terminal naman (kung mas gusto nyo):

```bash
./gradlew assembleDebug          # Mac / Linux
gradlew.bat assembleDebug        # Windows
```

### Direktang pag-install sa tablet

Isaksak ang tablet sa computer, buksan ang **USB debugging** sa Developer
options, tapos pindutin ang **Run ▶** sa Android Studio. Doon na mismo
mai-install.

Kung ililipat nyo lang ang APK file (hal. sa GDrive o USB): kailangang
payagan sa tablet ang **Install unknown apps** para sa app na gagamitin nyo
sa pag-open ng file.

---

## 3. Release APK (para sa totoong paggamit)

Ang debug APK ay puwede nang gamitin sa sariling tablet. Pero kung maraming
device o gusto nyong maayos ang update, gumawa ng signed release build:

1. **Build → Generate Signed Bundle / APK → APK → Create new…**
2. I-save ang keystore file at tandaan ang password.

   > ⚠️ **Huwag mawala ang keystore.** Kapag nawala, hindi na kayo
   > makakapag-release ng update sa parehong app — kailangan nang i-uninstall
   > muna ang luma bago mag-install ng bago, at mawawala ang data.

3. Piliin ang **release** build variant → Finish.
4. Lalabas sa `app/build/outputs/apk/release/app-release.apk`.

---

## 4. Unang paggamit

1. Buksan ang app. **PIN: `1234`**
2. Diretso sa **Settings → Staff & PINs** at palitan agad ang PIN na iyon.
3. Idagdag ang mga tauhan nyo at bigyan ng sariling PIN at role.
4. **Menu** at **Inventory** — palitan ang mga halimbawang presyo at recipe ng
   totoong presyo at costing nyo. Dito nakasalalay ang lahat ng margin at
   menu-engineering na resulta.

### Pag-setup ng printer

1. Sa tablet: **Settings → Bluetooth** → i-pair muna ang printer (karaniwang
   PIN ay `0000` o `1234`).
2. Balik sa app: **Settings → Receipt printer** → piliin ang printer sa listahan.
3. Pindutin ang **Test print**. Kung may lumabas na papel, ayos na.
4. I-on ang *Print the receipt automatically after each sale* at, kung may
   cash drawer, ang *Kick the cash drawer open on cash payments*.

Kung walang lumalabas sa listahan: hindi pa naka-pair ang printer, patay ang
Bluetooth, o hindi pa na-allow ang Bluetooth permission ng app
(**Android Settings → Apps → Juan Cafe Till → Permissions**).

---

## 5. Mahahalagang dapat tandaan

- **Nasa tablet lang ang data.** Walang sync sa ibang device. Kung
  mag-a-uninstall kayo o mag-clear ng app data, mawawala ang lahat.
- **Mag-export nang regular.** Sa **Reports → Export CSV**, **Receipts →
  Export CSV**, at **Time clock → Export timesheet**. Napupunta ang file sa
  `Downloads` folder ng tablet — i-back up nyo sa GDrive o email kada linggo.
  Ito ang backup nyo.
- **Isang tablet lang ang dapat gumamit sa isang pagkakataon.** Kung
  gagamitin nyo ang app sa dalawang tablet, magkahiwalay ang benta ng
  bawat isa.
- Ang **web version** (yung link) ay hiwalay at may sariling data. Puwede nyo
  iyong gamitin sa pagtingin ng reports mula sa bahay, pero hindi
  magkakonekta ang dalawa.

---

## 6. Kung ayaw mag-install ng Android Studio

May kasama nang GitHub Actions ang project na ito:

1. Gumawa ng libreng GitHub account.
2. Gumawa ng bagong repository at i-upload ang buong folder na ito.
3. Sa repo, pumunta sa **Actions** tab → **Build APK** → **Run workflow**.
4. Pagkatapos ng mga 5 minuto, i-download ang `juan-cafe-till-apk` sa ilalim
   ng run. Nandoon ang APK.

Debug-signed ang APK na iyon — puwede sa sariling tablet, hindi pang-Play Store.

---

## 7. Pag-update ng POS mismo

Ang buong till ay nasa iisang HTML file. Para mag-update:

1. Palitan ang `pos-page/index.html` ng bagong bersyon.
2. Patakbuhin: `python3 sync-assets.py pos-page/index.html`
3. Taasan ang `versionCode` at `versionName` sa `app/build.gradle`.
4. I-build ulit at i-install sa tablet.

Ginagawa ng `sync-assets.py` ang dalawang bagay: binabalot ang page sa isang
kumpletong HTML document, at tinatanggal ang web-font request — dahil kung
offline ang tablet, ang request na iyon ang magpapabagal sa pagbukas ng app.

---

## 8. Ano ang laman ng project

```
app/src/main/
  assets/index.html              buong POS (huwag i-edit dito — sa pos-page)
  java/ph/juancafe/till/
    MainActivity.kt              WebView, mga dialog, back button
    PosBridge.kt                 tulay ng JavaScript papunta sa tablet
    EscPos.kt                    Bluetooth printer at cash drawer
  res/                           icon, kulay, theme
pos-page/index.html              pinagmulan ng POS page
sync-assets.py                   kinokopya ang page papunta sa assets
```

Walang external na library ang app — WebView at Bluetooth lang mula mismo sa
Android. Kaya maliit ang APK at walang dependency na kailangang i-update.
