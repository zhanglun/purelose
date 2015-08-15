$(function() {
    var Todo = Backbone.Model.extend({
        urlRoot: '/todo/item',

        initialize: function() {},

        defaults: function() {
            return {
                title: 'empty todo...',
                done: false
            }
        },

        // 设置任务完成状态
        toggle: function() {
            this.save({
                done: !this.get('done')
            });
        }
    });

    // var test = new Todo({title:'删除按钮的bug还未解决'});
    // console.log(test.get('title'));
    // test.save();

    var TodoList = Backbone.Collection.extend({
        url: '/todo/list',
        model: Todo,

        done: function() {
            return this.where({
                done: true
            });
        },

        remaining: function() {
            return this.where({
                done: false
            });
        },

        nextOrder: function() {
            if (!this.lengtth) {
                return 1;
            }

            return this.last().get('order') + 1;
        },

        comparator: 'order'

    });

    var Todos = new TodoList();

    var TodoView = Backbone.View.extend({
        tagName: 'li',

        template: _.template($('#item-template').html(), {}),

        events: {
            'click .toggle': 'toggleDone',
            'click .view>label': 'edit',
            'dbclick .destory': 'clear',
            'keypress': 'updateOnEnter',
            'blur .edit': 'close'
        },

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destory', this.remove);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.toggleClass('done', this.model.get('done'));
            this.input = this.$('.edit');
            return this.$el
        },

        toggleDone: function() {
            this.model.toggle();
        },

        edit: function() {
            $(this.el).addClass('editing');
            this.input.focus();
        },

        // close
        close: function() {
            var value = this.input.val();
            if (!value) {
                this.clear();
            } else {
                this.model.save({
                    title: value
                });
                this.$el.removeClass('editing');
            }
        },

        updateOnEnter: function(e) {
            if (e.keyCode == 13) {
                this.close();
            }
        },

        clear: function() {
            this.model.destroy();
        }

    });

    var AppView = Backbone.View.extend({
        el: $('#todoapp'),

        statusTemplate: _.template($('#status-template').html(), {}),

        events: {
            'keypress #new-todo': 'createOnEnter',
            'click #clear-completed': 'clearCompleted',
            'click #toggle-all': 'toggleAllComplete'
        },

        // 在初始化过程中，绑定时间到Todos上

        initialize: function() {
            // this.statusTemplate = _.template($('#status-template').html(), {});
            this.input = this.$('#new-todo');
            this.allCheckbox = this.$('#toggle-all');

            this.listenTo(Todos, 'add', this.addOne);
            this.listenTo(Todos, 'reset', this.addAll);
            this.listenTo(Todos, 'all', this.render);

            this.footer = this.$('footer');
            this.main = $('#main');

            Todos.fetch();

        },

        render: function() {
            var done = Todos.done().length;
            var remaining = Todos.remaining.length;
            if (Todos.length) {
                this.main.show();
                this.footer.show();
                this.footer.html(this.statusTemplate({
                    done: done,
                    remaining: remaining
                }));
            } else {
                this.main.hide();
                this.footer.hide();
            }

            this.allCheckbox.checked = !remaining;
        },

        addOne: function(todo) {
            var view = new TodoView({
                model: todo
            });
            this.$('#todo-list').append(view.render());
        },

        addAll: function() {
            Todos.each(this.addOne, this);
        },

        newAttributes: function() {
            return {
                title: this.input.val(),
                order: Todos.nextorder(),
                donw: false
            }
        },

        createOnEnter: function(e) {;
            if (e.keyCode == 13) {
                if (!this.input.val()) {
                    return false;
                }

                // Todos.create({
                //     title: this.input.val(),
                //     order: Todos,
                //     done: false,
                // });
                var new_item = new Todo({
                    title: this.input.val(),
                    order: Todos,
                    done: false,
                });
                new_item.save();
                this.input.val('');
                this.addOne();
            }
        },

        renderNewTodo: function() {

        },

        clearCompleted: function() {
            _.invoke(Todos.done(), 'destroy');
            return false
        },

        toggleAllComplete: function() {
            var done = this.allCheckbox.checked;
            Todos.each(function(todo) {
                todo.save({
                    'done': done
                });
            });
        }

    });

    var App = new AppView();

});
