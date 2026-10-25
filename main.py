from config import MAX_REVIEW_ROUNDS
from core.logger import log
from core.state import WorkflowState
from core.workflow import Workflow


def main():
    print("=" * 60)
    print("  代码审查 Workflow（编码 → 审查 → 修复）")
    print("  输入以下任一内容，启动端到端流程：")
    print("    1) 直接粘贴代码")
    print("    2) 文件路径，如 examples/buggy.py")
    print("    3) 功能描述，如：写一个计算两个数相除的函数")
    print("=" * 60)

    raw = input("\n请输入：\n").strip()
    if not raw:
        print("未输入内容，退出。")
        return

    state = WorkflowState(raw_input=raw, max_iterations=MAX_REVIEW_ROUNDS)

    try:
        workflow = Workflow(state)
        result = workflow.run()
    except Exception as e:
        print(f"\n流程失败：{e}")
        return

    print("\n" + "=" * 60)
    print("最终代码：")
    print("=" * 60)
    print(result.code or "(空)")


if __name__ == "__main__":
    main()
