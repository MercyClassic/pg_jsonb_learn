import json

import pytest
from httpx import AsyncClient

from main import app


class CoreTests:
    async def test_get_empty_file_list(self, client: AsyncClient):
        response = await client.get(
            url=app.url_path_for('get_file_list'),
        )
        assert response.status_code == 200
        assert response.json() == {'files': []}

    async def test_create_file(self, client: AsyncClient):
        response = await client.post(
            url=app.url_path_for('post_file'),
        )
        assert response.status_code == 422

        with open('../tests/files/right_file.csv', 'rb') as f:
            response = await client.post(
                url=app.url_path_for('post_file'),
                files={'file': ('filename.csv', f, 'text/csv')},
            )
        assert response.status_code == 201

    async def test_get_file_list(self, client: AsyncClient):
        response = await client.get(app.url_path_for('get_file_list'))
        assert response.status_code == 200
        assert response.json() == {
            'files': [
                {
                    'id': 1,
                    'info': {
                        'columns': ['name', 'age', 'rate'],
                        'filename': f"{response.json()['files'][0]['info']['filename']}",
                        'size': '52',
                    },
                },
            ],
        }

    @staticmethod
    def get_rows(sort_by: str):
        rows = [
            {'age': 2, 'name': 'Barsik', 'rate': 8},
            {'age': 2, 'name': 'Masya', 'rate': 7},
            {'age': 4, 'name': 'Vanilla', 'rate': 10},
        ]
        if sort_by:
            rows = sorted(rows, key=lambda x: x[sort_by])
        return rows

    @pytest.mark.parametrize(
        'sort_by',
        [
            None,
            'name',
            'age',
            'rate',
        ],
    )
    async def test_get_file_detail(
        self,
        client: AsyncClient,
        sort_by: str,
    ):
        response = await client.get(
            url=app.url_path_for('get_file_detail', file_id=1),
            params={'sort_by': sort_by},
        )

        assert response.json() == {
            'file': {
                'id': 1,
                'info': {
                    'size': '52',
                    'columns': ['name', 'age', 'rate'],
                    'filename': f"{response.json()['file']['info']['filename']}",
                },
                'rows': self.get_rows(sort_by),
            },
        }

    async def test_file_not_found(self, client: AsyncClient):
        response = await client.get(
            url=app.url_path_for('get_file_detail', file_id=2),
        )
        assert response.status_code == 404
        assert response.json() == {'detail': 'File Not Found'}

    @pytest.mark.parametrize(
        'file_id, column, is_has',
        [
            (1, 'name', True),
            (1, 'abcd', False),
        ],
    )
    async def test_is_has_column(
        self,
        client: AsyncClient,
        file_id: int,
        column: str,
        is_has: bool,
    ):
        response = await client.post(
            url=app.url_path_for('column_exists', file_id=file_id),
            content=json.dumps(column),
        )
        assert response.json() == ({'result': is_has})
        assert response.status_code == 200
