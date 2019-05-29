$('[data-toggle="tooltip"]').tooltip();


var data = {
    "nodes":[
        {
            "frontNodeId":"node_01",
            "type":"realtime",
            "x":326.99617734375,
            "y":132.99494138183593,
            "className":"info",
            "config":{
                "name":"CPU检查",
                "sql":"sadfdf",
                "table_name":"asdf",
                "count_freq":"asdf",
                "waiting_time":"asdfasdf",
                "storages":"asdfasdf",
                "storages_args":"asdfasdf",
                "job_id":"asdfsd"
            }
        },
        {
            "frontNodeId":"node_ed511",
            "type":"datasource",
            "x":30,
            "y":136,
            "className":"invalid"
        },
        {
            "frontNodeId":"node_c36e9",
            "type":"realtime",
            "x":138.75,
            "y":130,
            "className":"invalid",
            "config":{
                "name":"内存"
            }
        },
        {
            "frontNodeId":"node_68e18",
            "type":"realtime",
            "x":528.7499615234375,
            "y":135.99619260253905,
            "className":"invalid",
            "config":{
                "name":"磁盘"
            }
        },
        {
            "frontNodeId":"node_47e58",
            "type":"offline",
            "x":708,
            "y":144,
            "className":"invalid"
        }
    ],
    "lines":[
        {
            "fromNodeId":"node_ed511",
            "toNodeId":"node_c36e9"
        },
        {
            "fromNodeId":"node_c36e9",
            "toNodeId":"node_01"
        },
        {
            "fromNodeId":"node_01",
            "toNodeId":"node_68e18"
        },
        {
            "fromNodeId":"node_68e18",
            "toNodeId":"node_47e58"
        }
    ]
}
var df = $('.dataflow').workFlow({
    data: data,
    onCreateNodeBefore: function (nodeInfo) {
        nodeInfo.config = {
            name: "节点"
        };
    },
    onCreateLineAfter: function(eln, info) {
        info.line.class = 'info'; //创建线条后设置线条的类为info
    }
});
$('.dataflow')
    .on('mouseenter', '.node', function() {
        var $this = $(this);
        $this.find('.toolsbar').removeClass('none');
    })
    .on('mouseleave', '.node', function() {
        var $this = $(this);
        $this.find('.toolsbar').addClass('none');
    })
    //删除节点
    .on('click', '.del', function(e) {
        if (confirm('确定删除？')) {
 
            df.remove({
                type: 'node',
                eln: $(this).parents('.node'),
            });
 
        }
    })
    //编辑节点
    .on('click', '.edit', function() {
        var id = $(this).closest('.toolsbar').attr('data-id'),
            data = df.getNodeVueById(id);
        if (!data.config) {
            data.config = {
                name: ''
            }
        }
        
        //dialog1.showModal();// 或者show(),这是有区别的
        dialog({
            width: 260,
            title: '编辑节点',
            content: '<input class="form-control" maxlength="20"/>',
            onshow: function() {
                $(this.node).find('input').val(data.config.name).focus();
            },
            ok: function() {
                data.config.name = $(this.node).find('input').val();
            },
        }).showModal();
    });
//获取结果
$('#save').click(function(event) {
    var nodes = df.getNodes().map(function(v, i) {
        return {
            frontNodeId: v.id,
            type: v.type,
            x: v.layout.x,
            y: v.layout.y,
            className: v.layout.class,
            config: v.config
        }
    });
    var lines = df.getLines().map(function(v, i) {
        return {
            fromNodeId: v.sourceId,
            toNodeId: v.targetId
        }
    });
    var data = {
        nodes: nodes,
        lines: lines
    }
    $('#result').val(JSON.stringify(data)).focus();
 
});