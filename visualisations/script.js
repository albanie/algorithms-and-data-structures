(function () {

    // Make things really fast
    var step = 10 ;
    var delay = 0.001;

    d3.select('#svg').on('click', function () {
        draw('svg');
    });
    // d3.select('#canvas').on('click', function () {
    //     draw('canvas');
    // });
    // if (d3.resolution() > 1) {
    //     d3.select('#paper').append('label').html(
    //         "<input id='canvas-low' name='type' type='radio'><span>canvas low resolution</span>"
    //     );
    //     d3.select('#canvas-low').on('click', function () {
    //         draw('canvas', 1);
    //     });
    // }

    var originalInsert = d3.binaryTree.prototype.insert;


    d3.binaryTree.prototype.insert = function (node) {
        if (!this.root) {
            originalInsert.call(this, node);
            this.root.x = node.x;
            this.root.y = node.y;
            addNode(this.root);
        }
        else insertAnimation.call(this.root, node, this);
    };


    var generator = d3.randomUniform(0, 1),
        tree = d3.binaryTree(),
        radius = 5,
        node = {},
        maxDepth = 0,
        treeSize = 0,
        c1 = 0.5,
        c2 = 0.3,
        paper, pnodes, plinks, text, circle, x, y;

    var simulation = d3
            .forceSimulation()
            //.force("center", d3.forceCenter(0.5, 0.5))
            .force("body", d3.forceManyBody().strength(-0.002))
            .force("links", d3.forceLink().strength(0.2).distance(0.005))
            .force("x", d3.forceX(function (nd) {
                if (nd.parent) {
                    var x1 = nd.parent.parent ? nd.parent.parent.x : 0.5;
                    return c2*(c1 * nd.parent.x + (1 - c1) * x1) + (1 - c2)*0.5;
                }
                return 0.5;
            }).strength(function (nd) {
                var dp = nd.depth();
                if (!dp) return 5;
                return Math.min(0.005*(treeSize + 1), 5);
            }))
            .force("y", d3.forceY(function (nd) {
                return 0.1 + 0.8*(1 + nd.depth())/(maxDepth + 2);
            }).strength(function (nd) {
                if (!nd.depth())
                    return 5;
                return Math.min(0.5*(maxDepth + 1), 5);
            }))
            .on('tick', tick);


    d3.timeout(dropNode, delay);

    draw('svg');

    function draw(type, r) {

        var example = d3.select("#example"),
            width = d3.getSize(example.style('width')),
            height = Math.min(500, width);

        x = d3.scaleLinear().range([0, width]);
        y = d3.scaleLinear().range([0, height]);

        example.select('.paper').remove();

        paper = example
                .append(type)
                .classed('paper', true)
                .attr('width', width).attr('height', height).canvasResolution(r).canvas(true);

        paper.append('rect')
                .attr('width', width)
                .attr('height', height)
                .style('fill', '#fff');

        text = paper.append('g').append('text')
            .text('depth: 0')
            .style('font-size', '20px')
            .style('text-anchor', 'middle')
            .style('alignment-baseline', 'middle')
            .attr("transform", "translate(50, 50)");

        paper.append('g').classed('links', true).style("stroke-width", "0.5px");
        paper.append('g').classed('tree', true);

        circle = paper
                    .append('g')
                    .classed('node', true)
                    .append('circle')
                    .attr("r", 1.5*radius)
                    .style("stroke", "black")
                    .style("fill", "yellow");

        updateTree();
    }

    function tick () {
        if (pnodes) {
            plinks
                .attr("x1", function (d) {return x(d.source.x);})
                .attr("y1", function (d) {return y(d.source.y);})
                .attr("x2", function (d) {return x(d.target.x);})
                .attr("y2", function (d) {return y(d.target.y);});
            pnodes
                .attr("cx", function (d) {return x(d.x);})
                .attr("cy", function (d) {return y(d.y);});
        }
    }

    function insertAnimation (node, tree) {
        var self = this;
        node.x = self.x;
        node.y = self.y;
        updateNode();

        d3.timeout(function () {
            if (node.score > self.score) {
                if (self.right) return insertAnimation.call(self.right, node, tree);
            } else {
                if (self.left) return insertAnimation.call(self.left, node, tree);
            }
            tree.root = self.insert(node, function (nd) {
                d3.timeout(function () {
                    addNode(nd);
                });
            });
        }, 50);
    }

    function updateTree () {
        var circles = paper.select('g.tree').selectAll('circle')
                    .data(simulation.nodes()),
            lines = paper.select('g.links').selectAll('line')
                    .data(simulation.force('links').links());

        plinks = lines
            .enter()
            .append("line")
            .style("stroke", "black")
            .merge(lines);

        pnodes = circles
            .enter()
            .append("circle")
            .attr("r", radius)
            .style("stroke", "black")
            .merge(circles)
            .style("fill", function (d) {return d.red ? "red" : "black";});
    }

    function addNode (nd) {
        var nodes = simulation.nodes(),
            links = simulation.force('links');
        resetNode();
        if (nd.parent) {
            nd.x = nd.parent.x;
            nd.y = nd.parent.y;
        }
        maxDepth = tree.maxDepth();
        treeSize = tree.size();
        text.text('depth: ' + maxDepth)
        nodes.push(nd);
        simulation.nodes(nodes);
        links.links(tree.links());
        updateTree();
        dropNode();
        simulation.alphaTarget(0.3).restart();
    }

    function dropNode () {
        if (!node.x) resetNode();
        var target = tree.root ? tree.root.y : 0.5;
        node.y += step;
        if (node.y >= target)
            tree.insert(node);
        else {
            updateNode();
            d3.timeout(dropNode, delay);
        }
    }

    function resetNode() {
        node.x = 0.5;
        node.y = -0.15;
        node.score = generator();
    }

    function updateNode () {
        circle
            .attr("cx", x(node.x))
            .attr("cy", y(node.y))
    }
}());