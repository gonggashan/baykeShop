from django.urls import NoReverseMatch, reverse
from baykeshop.apps.system.models import BaykeSiteMenus


class DynamicMenu:
    
    def __init__(self, request) -> None:
        self._request = request
        self._user = request.user

    def is_authenticated(self):
        # 判断当前用户是否登录
        return self._user.is_authenticated
    
    def get_user_perms(self):
        # 获取当前用户的权限标识
        return (
            self._user.get_all_permissions() 
            if self.is_authenticated
            else set()
        )
        
    def _get_queryset(self):
        # 菜单的queryset数据
        return BaykeSiteMenus.objects.body()
    
    def get_permmenus(self):
        # 当前用户拥有权限的菜单
        menus = self._get_queryset()
        perms = self.get_user_perms()
        
        permmenus = []
        for menu in menus:
            if menu.permission:
                app_label = menu.permission.content_type.app_label
                codename = menu.permission.codename
                info = f"{app_label}.{codename}"
                if info in perms:
                    if menu.parent:
                        permmenus.append(menu.parent)
                    permmenus.append(menu)
        return set(permmenus)
    
    def get_queryset(self):
        return self._get_queryset().filter(id__in=[menu.id for menu in self.get_permmenus()])
    

class MenusMixins:
    """ 后端自定义菜单类 """
    def _build_menus(self, request):
        perm_menus = []
        menus_obj = DynamicMenu(request) 
        menus = menus_obj.get_queryset()
        
        for menu in menus:
            model_dict = {
                "id": menu.id,
                "name": menu.name,
                "app_label": menu.name,
                "icon": menu.icon,
                "parent": menu.parent.id if menu.parent else None,
                "expanded": False,
            }
            if menu.permission:
                app_label = menu.permission.content_type.app_label
                model = menu.permission.content_type.model_class()
                
                if model in self._registry.keys():
                    # 获取模型对应的ModelAdmin
                    model_admin = self._registry.get(menu.permission.content_type.model_class())
                    # 判断是否拥有该应用app的权限
                    has_module_perms = model_admin.has_module_permission(request)
                    if not has_module_perms:
                        continue
                    # 获取该模型的默认增删改查权限
                    perms = model_admin.get_model_perms(request)
                    if True not in perms.values():
                        continue
                    
                    info = (app_label, model._meta.model_name)
                    model_dict = {
                        "id": menu.id,
                        "model": model,
                        "name": menu.name,
                        "object_name": model._meta.object_name,
                        "perms": perms,
                        "icon": menu.icon,
                        "admin_url": None,
                        "add_url": None,
                        "parent": menu.parent.id if menu.parent else None,
                        "active": False
                    }
                        
                    if perms.get("change") or perms.get("view"):
                        model_dict["view_only"] = not perms.get("change")
                        try:
            
                            model_dict["admin_url"] = reverse(
                                "admin:%s_%s_changelist" % info, current_app=self.name
                            )
                            if request.path == model_dict.get("admin_url"):
                                model_dict['active'] = True
                                request.breadcrumbs = model_dict
                        except NoReverseMatch:
                            pass
                        
                    if perms.get("add"):
                        try:
                            model_dict["add_url"] = reverse(
                                "admin:%s_%s_add" % info, current_app=self.name
                            )
                        except NoReverseMatch:
                            pass
                else:
                    print(f'{model._meta.model_name}【{model._meta.verbose_name}】未在admin中注册，请先注册模型')
                if not model_dict["admin_url"]:
                    continue
            perm_menus.append(model_dict)
        perm_menus = self.generate_tree(perm_menus, None)
        return perm_menus
    
    def get_menus(self, request):
        return self._build_menus(request)
    
    def generate_tree(self, source, parent):
        """ 树形结构迭代"""
        tree = []
        for item in source:
            if item["parent"] == parent:
                item["models"] = self.generate_tree(source, item["id"])
                tree.append(item)
            self._traverse(item)
        return tree
                
    def _traverse(self, node):
        # 递归判断active并修改父类的expanded
        if 'models' in node and node['models']:
            for item in node['models']:
                if not item.get('active'):
                    continue
                node['expanded'] = True
                self._traverse(item)