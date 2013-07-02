# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

import web

from nailgun.db import db
from nailgun.errors import errors
from nailgun.api.models import Release
from nailgun.api.validators.release import ReleaseValidator
from nailgun.api.handlers.base import JSONHandler, content_json


class ReleaseHandler(JSONHandler):
    fields = (
        "id",
        "name",
        "version",
        "description",
        "state"
    )
    model = Release
    validator = ReleaseValidator

    @content_json
    def GET(self, release_id):
        release = self.get_object_or_404(Release, release_id)
        return self.render(release)

    @content_json
    def PUT(self, release_id):
        release = self.get_object_or_404(Release, release_id)

        data = self.checked_data()

        for key, value in data.iteritems():
            setattr(release, key, value)
        db().commit()
        return self.render(release)

    def DELETE(self, release_id):
        release = self.get_object_or_404(Release, release_id)
        db().delete(release)
        db().commit()
        raise web.webapi.HTTPError(
            status="204 No Content",
            data=""
        )


class ReleaseCollectionHandler(JSONHandler):

    validator = ReleaseValidator

    @content_json
    def GET(self):
        return map(
            ReleaseHandler.render,
            db().query(Release).all()
        )

    @content_json
    def POST(self):
        data = self.checked_data()

        release = Release()
        for key, value in data.iteritems():
            setattr(release, key, value)
        db().add(release)
        db().commit()
        raise web.webapi.created(json.dumps(
            ReleaseHandler.render(release),
            indent=4
        ))
