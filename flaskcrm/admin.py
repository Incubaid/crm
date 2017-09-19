"""
ADMIN INTERFACE RELATED LOGIC
"""


class AdminLinksMixin(object):
    ADMIN_EDIT_LINK = "/{modelname}/edit/?id={modelid}"
    ADMIN_LIST_LINK = "/{modelname}/"
    ADMIN_VIEW_LINK = "/{modelname}/details/?id={modelid}"

    ADMIN_CREATE_LINK = "/{modelname}/new/?id={modelid}"

    ADMIN_EDIT_LINK_MODAL = "/{modelname}/edit/?id={modelid}"  # &modal=True"
    ADMIN_VIEW_LINK_MODAL = "/{modelname}/details/?id={modelid}"
    ADMIN_CREATE_LINK_MODAL = "/{modelname}/new/?url=/{modelname}"

    def _format_link(self, link):
        return link.format(
            modelname=self.__class__.__name__.lower()
    )

    def admin_list_link(self):
        return self._format_link(AdminLinksMixin.ADMIN_LIST_LINK)

    def admin_edit_link(self):
        return self._format_link(AdminLinksMixin.ADMIN_EDIT_LINK)

    def admin_view_link(self):
        return self._format_link(AdminLinksMixin.ADMIN_VIEW_LINK)

    def admin_create_link(self):
        return self._format_link(AdminLinksMixin.ADMIN_CREATE_LINK)

    def admin_edit_link_modal(self):
        return self._format_link(AdminLinksMixin.ADMIN_EDIT_LINK_MODAL)

    def admin_view_link_modal(self):
        return self._format_link(AdminLinksMixin.ADMIN_VIEW_LINK_MODAL)

    def admin_create_link_modal(self):
        return self._format_link(AdminLinksMixin.ADMIN_CREATE_LINK_MODAL)
