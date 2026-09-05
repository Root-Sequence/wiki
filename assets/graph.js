(() => {
  "use strict";

  document.addEventListener("DOMContentLoaded", async () => {
    const host = document.getElementById("knowledge-graph");
    if (!host) return;

    const detail = document.getElementById("graph-detail");
    const search = document.getElementById("graph-search");
    const reset = document.getElementById("graph-reset");

    let graph;
    try {
      const response = await fetch(host.dataset.graphUrl || "../graph.json");
      graph = await response.json();
    } catch (error) {
      host.textContent = "The graph data could not be loaded.";
      console.error(error);
      return;
    }

    const width = 1100;
    const height = 720;
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "Root Sequence knowledge graph");
    host.replaceChildren(svg);

    const edgeLayer = document.createElementNS(svgNS, "g");
    const nodeLayer = document.createElementNS(svgNS, "g");
    edgeLayer.setAttribute("class", "graph-edges");
    nodeLayer.setAttribute("class", "graph-nodes");
    svg.append(edgeLayer, nodeLayer);

    const byId = new Map(graph.nodes.map((node) => [node.id, node]));
    const neighbors = new Map(graph.nodes.map((node) => [node.id, []]));

    const hash = (text) => {
      let h = 2166136261;
      for (const ch of text) {
        h ^= ch.charCodeAt(0);
        h = Math.imul(h, 16777619);
      }
      return h >>> 0;
    };

    graph.nodes.forEach((node, index) => {
      const h = hash(node.id);
      node.x = 120 + (h % 850);
      node.y = 90 + ((h >>> 10) % 520);
      node.vx = 0;
      node.vy = 0;
      node.fixed = false;
      node.index = index;
    });

    const edgeEls = graph.edges.map((edge) => {
      const line = document.createElementNS(svgNS, "line");
      line.setAttribute("class", `graph-edge relation-${edge.relation}`);
      edgeLayer.appendChild(line);
      neighbors.get(edge.source)?.push({ id: edge.target, relation: edge.relation });
      neighbors.get(edge.target)?.push({ id: edge.source, relation: edge.relation });
      return { edge, line };
    });

    const nodeEls = graph.nodes.map((node) => {
      const group = document.createElementNS(svgNS, "g");
      group.setAttribute("class", `graph-node kind-${node.kind}`);
      group.setAttribute("tabindex", "0");
      group.setAttribute("role", "button");
      group.setAttribute("aria-label", `${node.label}, ${node.kind}`);

      const circle = document.createElementNS(svgNS, "circle");
      circle.setAttribute("r", node.kind === "document" ? "10" : node.kind === "project" ? "8" : "6");

      const label = document.createElementNS(svgNS, "text");
      label.setAttribute("x", "11");
      label.setAttribute("y", "4");
      label.textContent = node.label;

      group.append(circle, label);
      nodeLayer.appendChild(group);

      const select = () => showDetail(node);
      group.addEventListener("click", select);
      group.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          select();
        }
      });

      let dragging = false;
      group.addEventListener("pointerdown", (event) => {
        dragging = true;
        node.fixed = true;
        group.setPointerCapture(event.pointerId);
      });
      group.addEventListener("pointermove", (event) => {
        if (!dragging) return;
        const rect = svg.getBoundingClientRect();
        node.x = ((event.clientX - rect.left) / rect.width) * width;
        node.y = ((event.clientY - rect.top) / rect.height) * height;
        node.vx = 0;
        node.vy = 0;
        render();
      });
      group.addEventListener("pointerup", (event) => {
        dragging = false;
        node.fixed = false;
        group.releasePointerCapture(event.pointerId);
      });

      return { node, group };
    });

    function showDetail(node) {
      const related = (neighbors.get(node.id) || [])
        .map(({ id, relation }) => {
          const other = byId.get(id);
          return other ? `<li><strong>${escapeHtml(other.label)}</strong> <span class="relation-label">${escapeHtml(relation)}</span></li>` : "";
        })
        .join("");
      const open = node.url ? `<p><a href="../${escapeAttr(node.url)}">Open ${escapeHtml(node.label)}</a></p>` : "";
      detail.innerHTML = `<h3>${escapeHtml(node.label)}</h3><p><code>${escapeHtml(node.kind)}</code></p>${open}${related ? `<ul>${related}</ul>` : "<p>No explicit relationships recorded yet.</p>"}`;
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]));
    }

    function escapeAttr(value) {
      return String(value).replace(/["<>]/g, "");
    }

    function tick() {
      const nodes = graph.nodes;
      const repulsion = 1300;
      const spring = 0.0045;
      const desired = 115;

      for (let i = 0; i < nodes.length; i += 1) {
        for (let j = i + 1; j < nodes.length; j += 1) {
          const a = nodes[i];
          const b = nodes[j];
          let dx = a.x - b.x;
          let dy = a.y - b.y;
          let d2 = dx * dx + dy * dy;
          if (d2 < 36) d2 = 36;
          const d = Math.sqrt(d2);
          const force = repulsion / d2;
          dx /= d;
          dy /= d;
          if (!a.fixed) {
            a.vx += dx * force;
            a.vy += dy * force;
          }
          if (!b.fixed) {
            b.vx -= dx * force;
            b.vy -= dy * force;
          }
        }
      }

      for (const edge of graph.edges) {
        const a = byId.get(edge.source);
        const b = byId.get(edge.target);
        if (!a || !b) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.max(1, Math.sqrt(dx * dx + dy * dy));
        const force = (d - desired) * spring;
        if (!a.fixed) {
          a.vx += (dx / d) * force;
          a.vy += (dy / d) * force;
        }
        if (!b.fixed) {
          b.vx -= (dx / d) * force;
          b.vy -= (dy / d) * force;
        }
      }

      for (const node of nodes) {
        if (!node.fixed) {
          node.vx += (width / 2 - node.x) * 0.0008;
          node.vy += (height / 2 - node.y) * 0.0008;
          node.vx *= 0.88;
          node.vy *= 0.88;
          node.x = Math.max(30, Math.min(width - 30, node.x + node.vx));
          node.y = Math.max(30, Math.min(height - 30, node.y + node.vy));
        }
      }
    }

    function render() {
      for (const { edge, line } of edgeEls) {
        const a = byId.get(edge.source);
        const b = byId.get(edge.target);
        if (!a || !b) continue;
        line.setAttribute("x1", a.x);
        line.setAttribute("y1", a.y);
        line.setAttribute("x2", b.x);
        line.setAttribute("y2", b.y);
      }
      for (const { node, group } of nodeEls) {
        group.setAttribute("transform", `translate(${node.x} ${node.y})`);
      }
    }

    let frame = 0;
    function animate() {
      if (frame < 260) {
        tick();
        render();
        frame += 1;
        requestAnimationFrame(animate);
      }
    }

    function applySearch() {
      const query = (search?.value || "").trim().toLowerCase();
      if (!query) {
        nodeEls.forEach(({ group }) => group.classList.remove("graph-dim", "graph-match"));
        edgeEls.forEach(({ line }) => line.classList.remove("graph-dim"));
        return;
      }
      const matches = new Set(graph.nodes.filter((n) => n.label.toLowerCase().includes(query)).map((n) => n.id));
      const visible = new Set(matches);
      for (const id of matches) {
        for (const neighbor of neighbors.get(id) || []) visible.add(neighbor.id);
      }
      nodeEls.forEach(({ node, group }) => {
        group.classList.toggle("graph-dim", !visible.has(node.id));
        group.classList.toggle("graph-match", matches.has(node.id));
      });
      edgeEls.forEach(({ edge, line }) => {
        line.classList.toggle("graph-dim", !(visible.has(edge.source) && visible.has(edge.target)));
      });
    }

    search?.addEventListener("input", applySearch);
    reset?.addEventListener("click", () => {
      if (search) search.value = "";
      applySearch();
      graph.nodes.forEach((node) => {
        const h = hash(node.id);
        node.x = 120 + (h % 850);
        node.y = 90 + ((h >>> 10) % 520);
        node.vx = 0;
        node.vy = 0;
      });
      frame = 0;
      animate();
    });

    render();
    animate();
  });
})();
