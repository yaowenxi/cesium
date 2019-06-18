from baselayer.app.handlers.base import BaseHandler
from .. import plot
from ..models import Featureset


class PlotFeaturesHandler(BaseHandler):
    def get(self, featureset_id):
        fset = Featureset.get_if_owned_by(featureset_id, self.current_user)
        features_to_plot = sorted(fset.features_list)[0:4]  # TODO from form
        docs_json, render_items = plot.feature_scatterplot(fset.file_uri,
                                                           features_to_plot)
        self.success({'docs_json': docs_json, 'render_items': render_items})
