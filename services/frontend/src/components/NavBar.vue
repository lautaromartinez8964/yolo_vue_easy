<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark shadow-sm">
      <div class="container">
        <!-- 品牌Logo -->
        <router-link class="navbar-brand" to="/">
          <i class="fas fa-bolt"></i> FastAPI & Vue
        </router-link>

        <!-- 移动端切换按钮 -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarCollapse">
          <!-- 左侧导航 (未登录) -->
          <ul v-if="!isLoggedIn" class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <i class="fas fa-home"></i> Home
              </router-link>
            </li>
          </ul>

          <!-- 左侧导航 (已登录) -->
          <ul v-if="isLoggedIn" class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <i class="fas fa-home"></i> Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/dashboard">
                <i class="fas fa-tachometer-alt"></i> Dashboard
              </router-link>
            </li>
          </ul>

          <!-- 右侧导航 -->
          <ul class="navbar-nav ms-auto mb-2 mb-md-0">
            <!-- 未登录状态 -->
            <template v-if="!isLoggedIn">
              <li class="nav-item">
                <router-link class="nav-link" to="/register">
                  <i class="fas fa-user-plus"></i> Register
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/login">
                  <i class="fas fa-sign-in-alt"></i> Log In
                </router-link>
              </li>
            </template>

            <!-- 已登录状态：使用下拉菜单展示用户信息 -->
            <template v-if="isLoggedIn">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="fas fa-user-circle"></i> Welcome, {{ user.username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDropdown">
                  <li>
                    <router-link class="dropdown-item" to="/profile">
                      <i class="fas fa-user-cog"></i> My Profile
                    </router-link>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item" @click="logout">
                      <i class="fas fa-sign-out-alt"></i> Log Out
                    </a>
                  </li>
                </ul>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

// 使用 Composition API 获取 store 和 router 实例
const store = useStore();
const router = useRouter();

// 从 store 的 getters 中获取响应式数据
const isLoggedIn = computed(() => store.getters.isAuthenticated);
const user = computed(() => store.getters.stateUser);

// 登出方法
const logout = async () => {
  await store.dispatch('logOut');
  // 登出后重定向到登录页
  router.push('/login');
};
</script>

<style scoped>
/* 为激活的路由链接添加更醒目的样式 */
.router-link-exact-active {
  color: #ffffff !important;
  font-weight: bold;
  border-bottom: 2px solid #42b983; /* Vue 绿色主题色 */
}

/* 调整下拉菜单项的图标间距 */
.dropdown-item i {
  margin-right: 8px;
}

/* 调整导航链接的图标间距 */
.nav-link i {
  margin-right: 5px;
}

/* 确保登出链接有手型光标 */
.dropdown-item {
  cursor: pointer;
}
</style>
