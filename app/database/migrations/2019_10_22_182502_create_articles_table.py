from orator.migrations import Migration


class CreateArticlesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('articles') as table:
            table.increments('id')
            table.string('company_name')
            table.string('base_url', 255)
            table.string('url', 255)
            table.string('title', 512)
            table.datetime('published_at').nullable()
            table.integer('hatena_bookmark_count').unsigned()
            table.datetime('hatena_bookmark_newest_comment_at').nullable()
            table.datetime('hatena_bookmark_oldest_comment_at').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('articles')
