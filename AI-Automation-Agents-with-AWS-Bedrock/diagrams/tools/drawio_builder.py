"""Build rich draw.io XML with AWS aws4 stencils + teaching annotations."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

SHAPES = {
    "user": "mxgraph.aws4.user",
    "client": "mxgraph.aws4.client",
    "api_gateway": "mxgraph.aws4.api_gateway",
    "lambda": "mxgraph.aws4.lambda",
    "step_functions": "mxgraph.aws4.step_functions",
    "eventbridge": "mxgraph.aws4.eventbridge",
    "dynamodb": "mxgraph.aws4.dynamodb",
    "s3": "mxgraph.aws4.s3",
    "cloudwatch": "mxgraph.aws4.cloudwatch",
    "iam": "mxgraph.aws4.identity_and_access_management",
    "bedrock": "mxgraph.aws4.bedrock",
    "cognito": "mxgraph.aws4.cognito",
    "sns": "mxgraph.aws4.sns",
    "sqs": "mxgraph.aws4.sqs",
    "waf": "mxgraph.aws4.waf",
    "vpc": "mxgraph.aws4.vpc",
    "document": "mxgraph.aws4.document",
    "secrets": "mxgraph.aws4.secrets_manager",
    "kms": "mxgraph.aws4.key_management_service",
    "generic": "mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.generic",
}

BASE_STYLE = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;"
    "strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;"
    "align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;pointerEvents=1;"
)

FILL = {
    "orange": "#D86613",
    "blue": "#527FFF",
    "green": "#248814",
    "purple": "#8C4FFF",
    "red": "#DD3522",
    "gray": "#879196",
    "dark": "#232F3E",
    "teal": "#00A6A6",
}


def xml_value(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("\n", "&#10;")
    )


def aws_style(shape: str, fill: str = "orange") -> str:
    hex_fill = FILL.get(fill, fill if str(fill).startswith("#") else FILL["orange"])
    return f"{BASE_STYLE}fillColor={hex_fill};shape={SHAPES.get(shape, shape)};"


@dataclass
class Node:
    id: str
    label: str
    shape: str
    x: int
    y: int
    w: int = 72
    h: int = 72
    fill: str = "orange"
    sublabel: str = ""  # second line under icon


@dataclass
class Edge:
    id: str
    source: str
    target: str
    label: str = ""
    dashed: bool = False
    color: str = "#232F3E"
    bold: bool = False


@dataclass
class Zone:
    """Swimlane / grouping region."""
    id: str
    title: str
    x: int
    y: int
    w: int
    h: int
    fill: str = "#F7F8F8"
    border: str = "#879196"


@dataclass
class Box:
    id: str
    label: str
    x: int
    y: int
    w: int
    h: int
    style: str = "neutral"  # neutral, code, danger, success, legend, objective


@dataclass
class StepBadge:
    number: int
    x: int
    y: int
    label: str = ""


@dataclass
class Diagram:
    name: str
    title: str
    subtitle: str = ""
    width: int = 1600
    height: int = 1100
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    boxes: list[Box] = field(default_factory=list)
    zones: list[Zone] = field(default_factory=list)
    steps: list[StepBadge] = field(default_factory=list)
    notes: list[Box] = field(default_factory=list)  # callouts


BOX_STYLES = {
    "neutral": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F2F3F3;strokeColor=#879196;align=left;verticalAlign=top;fontSize=10;spacingLeft=10;spacingTop=8;",
    "code": "rounded=0;whiteSpace=wrap;html=1;fillColor=#232F3E;fontColor=#FFFFFF;strokeColor=#232F3E;align=left;verticalAlign=top;fontSize=9;fontFamily=Courier New;spacingLeft=8;spacingTop=6;",
    "danger": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FADBD8;strokeColor=#DD3522;align=left;verticalAlign=top;fontSize=10;spacingLeft=10;spacingTop=8;",
    "success": "rounded=1;whiteSpace=wrap;html=1;fillColor=#E9F7EF;strokeColor=#248814;align=left;verticalAlign=top;fontSize=10;spacingLeft=10;spacingTop=8;",
    "legend": "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#232F3E;align=left;verticalAlign=top;fontSize=10;spacingLeft=10;spacingTop=8;",
    "objective": "rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F4FD;strokeColor=#527FFF;align=left;verticalAlign=top;fontSize=11;fontStyle=1;spacingLeft=10;spacingTop=8;",
    "instructor": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF8E6;strokeColor=#FFB800;align=left;verticalAlign=top;fontSize=10;spacingLeft=10;spacingTop=8;",
    "student": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F3E8FF;strokeColor=#8C4FFF;align=left;verticalAlign=top;fontSize=10;spacingLeft=10;spacingTop=8;",
}


class DrawioBuilder:
    def __init__(self, diagram: Diagram):
        self.d = diagram
        self._id = 100

    def _nid(self) -> str:
        self._id += 1
        return str(self._id)

    def build(self) -> str:
        root = ET.Element(
            "mxfile",
            {
                "host": "app.diagrams.net",
                "agent": "BayAreaLa8s-Detailed-Diagrams",
                "version": "24.7.0",
                "type": "device",
            },
        )
        diagram_el = ET.SubElement(root, "diagram", {"id": self.d.name, "name": self.d.title[:60]})
        diagram_el.set("compressed", "false")

        model = ET.SubElement(
            diagram_el,
            "mxGraphModel",
            {
                "dx": "1600", "dy": "1100", "grid": "1", "gridSize": "10",
                "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
                "page": "1", "pageScale": "1",
                "pageWidth": str(self.d.width), "pageHeight": str(self.d.height),
            },
        )
        root_cells = ET.SubElement(model, "root")
        ET.SubElement(root_cells, "mxCell", {"id": "0"})
        ET.SubElement(root_cells, "mxCell", {"id": "1", "parent": "0"})

        self._add_text(
            root_cells,
            self.d.title,
            40, 16, self.d.width - 80, 36,
            "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=20;fontStyle=1;fontColor=#232F3E;",
        )
        if self.d.subtitle:
            self._add_text(
                root_cells,
                self.d.subtitle,
                40, 48, self.d.width - 80, 28,
                "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=12;fontColor=#565656;",
            )

        y_offset = 72 if self.d.subtitle else 56

        for zone in self.d.zones:
            zy = zone.y + (y_offset - 56)
            self._add_box_cell(
                root_cells, zone.id, zone.title, zone.x, zy, zone.w, zone.h,
                f"rounded=1;whiteSpace=wrap;html=1;fillColor={zone.fill};strokeColor={zone.border};"
                "verticalAlign=top;fontSize=12;fontStyle=1;fontColor=#232F3E;align=left;spacingLeft=12;spacingTop=10;dashed=1;",
            )

        for box in self.d.boxes:
            style = BOX_STYLES.get(box.style, BOX_STYLES["neutral"])
            self._add_box_cell(root_cells, box.id, box.label, box.x, box.y, box.w, box.h, style)

        for note in self.d.notes:
            style = BOX_STYLES.get(note.style, BOX_STYLES["instructor"])
            self._add_box_cell(root_cells, note.id, note.label, note.x, note.y, note.w, note.h, style)

        for step in self.d.steps:
            sid = f"step{step.number}"
            self._add_text(
                root_cells,
                str(step.number),
                step.x, step.y, 28, 28,
                "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#232F3E;fontColor=#FFFFFF;"
                "strokeColor=#232F3E;fontSize=12;fontStyle=1;align=center;",
            )
            if step.label:
                self._add_text(
                    root_cells, step.label, step.x + 32, step.y + 4, 200, 24,
                    "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#232F3E;",
                )

        for node in self.d.nodes:
            label = node.label
            if node.sublabel:
                label = f"{node.label}&#10;{xml_value(node.sublabel)}"
            style = aws_style(node.shape, node.fill)
            cell = ET.SubElement(
                root_cells, "mxCell",
                {"id": node.id, "value": xml_value(label) if not node.sublabel else label,
                 "style": style, "vertex": "1", "parent": "1"},
            )
            cell.append(ET.Element("mxGeometry", {
                "x": str(node.x), "y": str(node.y),
                "width": str(node.w), "height": str(node.h), "as": "geometry",
            }))

        for edge in self.d.edges:
            style = (
                f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
                f"html=1;strokeColor={edge.color};fontColor={edge.color};fontSize=10;"
            )
            if edge.dashed:
                style += "dashed=1;dashPattern=8 4;"
            if edge.bold:
                style += "strokeWidth=2;"
            cell = ET.SubElement(
                root_cells, "mxCell",
                {"id": edge.id, "value": xml_value(edge.label), "style": style,
                 "edge": "1", "parent": "1", "source": edge.source, "target": edge.target},
            )
            cell.append(ET.Element("mxGeometry", {"relative": "1", "as": "geometry"}))

        ET.indent(root, space="  ")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode")

    def _add_text(self, parent, value: str, x: int, y: int, w: int, h: int, style: str) -> None:
        cid = self._nid()
        cell = ET.SubElement(
            parent, "mxCell",
            {"id": cid, "value": xml_value(value), "style": style, "vertex": "1", "parent": "1"},
        )
        cell.append(ET.Element("mxGeometry", {
            "x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry",
        }))

    def _add_box_cell(self, parent, cid: str, value: str, x: int, y: int, w: int, h: int, style: str) -> None:
        cell = ET.SubElement(
            parent, "mxCell",
            {"id": cid, "value": xml_value(value), "style": style, "vertex": "1", "parent": "1"},
        )
        cell.append(ET.Element("mxGeometry", {
            "x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry",
        }))
