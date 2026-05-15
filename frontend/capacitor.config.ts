import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.huatpick.app',
  appName: 'HuatPick',
  webDir: 'build',
  // Optional: When set, the native app loads from this remote URL instead of
  // the bundled build. Switch to undefined for a fully offline app.
  // server: {
  //   url: 'https://19393f19-3c96-4174-89da-c04f3489693e.preview.emergentagent.com',
  //   cleartext: false,
  // },
  ios: {
    contentInset: 'always',
    backgroundColor: '#FFFFFF',
  },
  android: {
    backgroundColor: '#FFFFFF',
    allowMixedContent: false,
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 1200,
      launchAutoHide: true,
      backgroundColor: '#FFFFFF',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: false,
      splashFullScreen: false,
      splashImmersive: false,
    },
    StatusBar: {
      style: 'DEFAULT',
      backgroundColor: '#FFFFFF',
      overlaysWebView: false,
    },
  },
};

export default config;
