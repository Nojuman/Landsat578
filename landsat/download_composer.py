# ===============================================================================
# Copyright 2017 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================


import os

import usgs_download
from web_tools import convert_lat_lon_wrs2pr


class InvalidPathRowData(Exception):
    pass


def download_landsat(start_end_tuple, satellite, path_row_list=None, lat_lon_tuple=None,
                     output_path=None,  usgs_creds=None, dry_run=False):

    start_date, end_date = start_end_tuple[0], start_end_tuple[1]

    if path_row_list:
        image_index = path_row_list

    elif lat_lon_tuple:
        image_index = [convert_lat_lon_wrs2pr(lat_lon_tuple)]

    else:
        raise InvalidPathRowData('Must give path/row tuple, lat/lon tuple plus row/path \n'
                                 'shapefile, or a path/rows shapefile!')

    for tile in image_index:

        scenes_list = usgs_download.get_candidate_scenes_list(tile, satellite, start_date, end_date)

        if dry_run:

            return scenes_list

        else:

            destination_path = os.path.join(output_path, 'd_{}_{}'.format(tile[0], tile[1]))

            if not os.path.exists(destination_path):
                print 'making dir: {}'.format(destination_path)
                os.mkdir(destination_path)

            usgs_download.down_usgs_by_list(scenes_list, destination_path, usgs_creds)

            return None


if __name__ == 'main':
    pass

# ===============================================================================